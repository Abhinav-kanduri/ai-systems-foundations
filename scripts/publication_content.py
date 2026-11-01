"""Discover and render publications without exposing unpublished source files."""
from __future__ import annotations

import copy
import html
import json
import math
import re
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

import bleach
import markdown
import yaml
from latex2mathml.converter import convert as convert_math

from publication_model import PublicationError, parse_date, publicly_available, validate_metadata, validate_relationships, validate_taxonomy


class MetadataLoader(yaml.SafeLoader):
    pass


def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise PublicationError(f"duplicate frontmatter key '{key}'")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


MetadataLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)
MetadataLoader.add_constructor("tag:yaml.org,2002:timestamp", lambda loader, node: loader.construct_scalar(node))


def split_frontmatter(text):
    match = re.match(r"\A---\s*\r?\n(.*?)\r?\n---\s*(?:\r?\n|$)", text, re.S)
    if not match:
        return None, text
    try:
        metadata = yaml.load(match[1], Loader=MetadataLoader)
    except yaml.YAMLError as error:
        raise PublicationError(f"invalid YAML frontmatter: {error}") from error
    if not isinstance(metadata, dict):
        raise PublicationError("frontmatter must be a metadata object")
    return metadata, text[match.end():]


MATH_TAGS = {
    "math", "mrow", "mi", "mn", "mo", "mtext", "mspace", "ms", "mfrac", "msqrt",
    "mroot", "msub", "msup", "msubsup", "munder", "mover", "munderover", "mtable",
    "mtr", "mtd", "mstyle", "mpadded", "mphantom", "menclose", "semantics", "annotation",
    "mfenced", "mmultiscripts", "mprescripts", "none", "mlabeledtr",
}
HTML_TAGS = {
    "p", "a", "h1", "h2", "h3", "h4", "h5", "h6", "ul", "ol", "li", "blockquote",
    "strong", "em", "del", "s", "code", "pre", "hr", "br", "table", "thead", "tbody",
    "tr", "th", "td", "img", "figure", "figcaption", "div", "span", "sup", "sub",
    "details", "summary", "kbd", "dl", "dt", "dd", "abbr",
}


def sanitize_attributes(tag, name, value):
    if name in {"id", "class", "title", "aria-label"}:
        return True
    if tag == "a" and name in {"href", "rel"}:
        return not value.strip().startswith("//")
    if tag == "img" and name in {"src", "alt", "width", "height", "loading"}:
        return not value.strip().startswith("//")
    if tag in {"th", "td"} and name in {"colspan", "rowspan"}:
        return True
    if tag in MATH_TAGS and name in {"xmlns", "display", "mathvariant", "mathsize", "stretchy", "fence", "separator", "form", "accent", "accentunder", "columnalign", "rowalign", "columnspacing", "rowspacing", "linethickness", "width", "height", "depth", "notation", "encoding"}:
        return True
    return False


class PlainText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)


def plain_text(value):
    parser = PlainText()
    parser.feed(value)
    return " ".join(" ".join(parser.parts).split())


def render_markdown(body):
    """Render code, tables, images, citations and native MathML, then sanitize."""
    math_fragments = {}

    def math_placeholder(source, display=False):
        key = f"PUBMATHPLACEHOLDER{len(math_fragments)}TOKEN"
        try:
            math_fragments[key] = convert_math(source.strip(), display="block" if display else "inline")
        except Exception as error:
            raise PublicationError(f"invalid mathematical expression: {source[:80]} ({error})") from error
        return key

    # Protect fenced code and inline code before processing math delimiters.
    code_fragments = {}
    def protect(match):
        key = f"PUBCODEPLACEHOLDER{len(code_fragments)}TOKEN"
        code_fragments[key] = match[0]
        return key
    text = re.sub(r"(?ms)^(`{3,}|~{3,})[^\n]*\n.*?^\1\s*$|`[^`\n]+`", protect, body)
    text = re.sub(r"(?ms)^\$\$\s*\n(.*?)\n\$\$\s*$", lambda m: math_placeholder(m[1], True), text)
    text = re.sub(r"(?<!\\)\$([^$\n]+?)(?<!\\)\$", lambda m: math_placeholder(m[1]), text)
    for key, value in code_fragments.items():
        text = text.replace(key, value)
    engine = markdown.Markdown(extensions=["extra", "toc", "codehilite", "sane_lists"], extension_configs={"toc": {"permalink": True}, "codehilite": {"guess_lang": False, "css_class": "codehilite"}})
    rendered = engine.convert(text)
    for key, value in math_fragments.items():
        rendered = rendered.replace(key, value)
    rendered = bleach.clean(rendered, tags=HTML_TAGS | MATH_TAGS, attributes=sanitize_attributes, protocols={"http", "https", "mailto"}, strip=True, strip_comments=True)
    rendered = re.sub(r"<img(?![^>]*\bloading=)", '<img loading="lazy"', rendered)
    toc = []
    def flatten(items):
        for item in items:
            toc.append({"id": item["id"], "title": plain_text(item["name"]), "level": item["level"]})
            flatten(item.get("children", []))
    flatten(engine.toc_tokens)
    return rendered, toc


def read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise PublicationError(f"{path}: {error}") from error


def load_library(root, now=None):
    root = Path(root).resolve()
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        raise PublicationError("build time must be timezone-aware")
    site = read_json(root / "content/site.json")
    if not re.fullmatch(r"https?://[^?#]+/", site.get("siteUrl", "")):
        raise PublicationError("siteUrl must be an absolute HTTP(S) URL ending in /")
    taxonomy = read_json(root / "content/taxonomy.json")
    validate_taxonomy(taxonomy)
    schema = read_json(root / "content/publication.schema.json")
    registry = read_json(root / "content/url-registry.json")
    categories = {c["id"]: c for c in taxonomy["categories"]}
    types = {t["id"]: t for t in taxonomy["publicationTypes"]}
    records, errors = [], []
    for folder in ("articles", "guides"):
        for path in sorted((root / "content" / folder).rglob("*.md")):
            try:
                if not path.resolve().is_relative_to(root / "content" / folder):
                    raise PublicationError("source symlink leaves content directory")
                metadata, body = split_frontmatter(path.read_text(encoding="utf-8"))
                sidecar = path.with_name("publication.json") if path.name == "README.md" else path.with_suffix(".json")
                if sidecar.exists():
                    if metadata is not None:
                        raise PublicationError("use either frontmatter or a metadata sidecar, not both")
                    metadata = read_json(sidecar)
                if metadata is None:
                    continue
                p = validate_metadata(metadata, schema, categories, types, path.relative_to(root).as_posix())
                p.setdefault("reader", "article")
                if p["reader"] == "fde" and p["id"] != "fde-field-guide":
                    raise PublicationError("the existing FDE reader is reserved for fde-field-guide")
                p.setdefault("author", site.get("defaultAuthor"))
                p["source"] = path.relative_to(root).as_posix()
                p["body"] = body
                if p['reader'] == 'fde':
                    p['chapterSlugs'] = [re.sub(r'-+', '-', re.sub(r'\s+', '-', re.sub(r'[^a-z0-9\s-]', '', title.lower()).strip())) for title in re.findall(r'^# (\d+\..+)$', body, re.M)]
                p.setdefault("readingTime", max(1, math.ceil(len(re.findall(r"\b[\w'-]+\b", body)) / 220)))
                p["html"], p["tableOfContents"] = render_markdown(body)
                p["searchText"] = plain_text(p["html"])
                p["canonicalUrl"] = p.get("canonicalUrl") or (site["siteUrl"] if p["reader"] == "fde" else site["siteUrl"] + "publications/" + p["slug"] + "/")
                p["url"] = "../../#end-to-end-fde-learning-map" if p["reader"] == "fde" else None
                records.append(p)
            except PublicationError as error:
                errors.extend(f"{path.relative_to(root)}: {e}" for e in error.errors)
    if errors:
        raise PublicationError(errors)
    collections = {kind: [read_json(p) for p in sorted((root / "content" / folder).glob("*.json"))] for kind, folder in (("series", "series"), ("paths", "learning-paths"))}
    validate_relationships(records, collections, registry)
    visible = sorted((p for p in records if publicly_available(p, now)), key=lambda p: (-parse_date(p["publishedAt"]).timestamp(), p["id"]))
    routes = [p for p in records if publicly_available(p, now, include_archived=True)]
    visible_ids = {p["id"] for p in visible}
    public_collections = {}
    for kind, values in collections.items():
        public_collections[kind] = []
        for collection in values:
            members = [i for i in collection["publicationIds"] if i in visible_ids]
            if collection.get("status", "published") == "published" and members:
                c = dict(collection, publicationIds=members)
                c["readingTime"] = sum(p["readingTime"] for p in visible if p["id"] in members)
                public_collections[kind].append(c)
    return {"site": site, "taxonomy": taxonomy, "records": records, "publications": visible, "routes": routes, "collections": public_collections, "now": now}


def public_record(p):
    result = {k: copy.deepcopy(v) for k, v in p.items() if k not in {"source", "body", "html"}}
    result["status"] = "archived" if p["status"] == "archived" else "published"
    return result
