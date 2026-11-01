"""Publication metadata validation; independent of rendering and file discovery."""
from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from jsonschema import Draft202012Validator, FormatChecker

RESERVED = {"latest", "topics", "series", "paths", "feed", "index", "assets", "search", "preview", "about"}
STATUSES = {"draft", "review", "scheduled", "published", "archived"}


class PublicationError(ValueError):
    def __init__(self, errors):
        self.errors = errors if isinstance(errors, list) else [str(errors)]
        super().__init__("\n".join(self.errors))


def slugify(value):
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def parse_date(value):
    if not value:
        return None
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return parsed.replace(tzinfo=timezone.utc) if parsed.tzinfo is None else parsed.astimezone(timezone.utc)


def validate_metadata(meta, schema, categories, types, source="publication"):
    errors = []
    for error in Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(meta):
        field = ".".join(str(part) for part in error.absolute_path) or "metadata"
        errors.append(f"{source}: {field}: {error.message}")
    if errors:
        raise PublicationError(errors)
    result = dict(meta)
    result.setdefault("slug", slugify(result["title"]))
    if not result["slug"] or result["slug"] in RESERVED:
        errors.append(f"{source}: slug '{result['slug']}' is empty or reserved")
    for field in ("publishedAt", "updatedAt"):
        try:
            parse_date(result.get(field))
        except (ValueError, TypeError):
            errors.append(f"{source}: {field} must be a real ISO date or timezone-qualified timestamp")
    if result["status"] == "scheduled" and "T" not in str(result.get("publishedAt", "")):
        errors.append(f"{source}: scheduled publication requires a timestamp with timezone")
    if result.get("updatedAt") and result.get("publishedAt") and not errors:
        if parse_date(result["updatedAt"]) < parse_date(result["publishedAt"]):
            errors.append(f"{source}: updatedAt cannot precede publishedAt")
    subjects = [result["primaryCategory"], *result.get("secondaryCategories", [])]
    for category in subjects:
        if category not in categories:
            errors.append(f"{source}: unknown category '{category}'")
    if len(set(subjects)) != len(subjects):
        errors.append(f"{source}: primary category cannot repeat as a secondary category")
    if result["publicationType"] not in types:
        errors.append(f"{source}: unknown publicationType '{result['publicationType']}'")
    for revision in result.get("revisions", []):
        try:
            if not parse_date(revision["date"]):
                raise ValueError()
        except (ValueError, TypeError):
            errors.append(f"{source}: revision date must be a real ISO date")
    if errors:
        raise PublicationError(errors)
    return result


def validate_taxonomy(taxonomy):
    errors = []
    for group in ("categories", "publicationTypes"):
        ids, slugs = set(), set()
        for item in taxonomy.get(group, []):
            if not all(isinstance(item.get(k), str) and item[k].strip() for k in ("id", "title")):
                errors.append(f"taxonomy: {group} requires nonempty id and title")
                continue
            slug = item.get("slug", item["id"])
            if item["id"] in ids or slug in slugs or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
                errors.append(f"taxonomy: duplicate or invalid {group} identity '{item['id']}'")
            ids.add(item["id"])
            slugs.add(slug)
    categories = {x["id"]: x for x in taxonomy.get("categories", [])}
    for item in categories.values():
        seen, parent = {item["id"]}, item.get("parentId")
        while parent:
            if parent not in categories or parent in seen:
                errors.append(f"taxonomy: invalid or circular parent for '{item['id']}'")
                break
            seen.add(parent)
            parent = categories[parent].get("parentId")
    if errors:
        raise PublicationError(errors)


def validate_relationships(publications, collections, registry=None):
    errors, by_id, slugs, canonicals = [], {}, set(), set()
    for p in publications:
        if p["id"] in by_id:
            errors.append(f"duplicate publication id '{p['id']}'")
        if p["slug"] in slugs:
            errors.append(f"duplicate publication slug '{p['slug']}'")
        by_id[p["id"]] = p
        slugs.add(p["slug"])
        canonical = p.get("canonicalUrl")
        if canonical and canonical in canonicals:
            errors.append(f"duplicate canonical URL '{canonical}'")
        if canonical:
            canonicals.add(canonical)
        locked = (registry or {}).get(p["id"])
        if locked and (locked["slug"] != p["slug"] or (canonical and locked["canonicalUrl"] != canonical)):
            errors.append(f"{p['id']}: published URL is locked; add an explicit redirect before changing it")
    series = {}
    for kind, values in collections.items():
        ids, collection_slugs = set(), set()
        for c in values:
            if not all(isinstance(c.get(k), str) and c[k].strip() for k in ("id", "slug", "title", "description")):
                errors.append(f"{kind}: collection requires id, slug, title, description")
                continue
            if c["id"] in ids or c["slug"] in collection_slugs or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", c["slug"]):
                errors.append(f"{kind}: duplicate or invalid collection '{c['id']}'")
            ids.add(c["id"])
            collection_slugs.add(c["slug"])
            members = c.get("publicationIds", [])
            if not isinstance(members, list) or not members or len(set(members)) != len(members):
                errors.append(f"{kind}/{c['id']}: requires unique ordered publicationIds")
                continue
            if c.get("status", "published") not in {"draft", "published", "archived"}:
                errors.append(f"{kind}/{c['id']}: invalid collection status")
            for member in members:
                if member not in by_id:
                    errors.append(f"{kind}/{c['id']}: unknown publication '{member}'")
            if kind == "series":
                series[c["id"]] = c
    for p in publications:
        for related in p.get("relatedPublicationIds", []):
            if related == p["id"] or related not in by_id:
                errors.append(f"{p['id']}: invalid related publication '{related}'")
        if p.get("seriesId"):
            c = series.get(p["seriesId"])
            if not c or p["id"] not in c.get("publicationIds", []):
                errors.append(f"{p['id']}: seriesId must reference a series containing this publication")
            elif p.get("seriesOrder") and c["publicationIds"].index(p["id"]) + 1 != p["seriesOrder"]:
                errors.append(f"{p['id']}: seriesOrder disagrees with explicit series ordering")
        elif p.get("seriesOrder"):
            errors.append(f"{p['id']}: seriesOrder requires seriesId")
    if errors:
        raise PublicationError(errors)


def publicly_available(publication, now, include_archived=False):
    status = publication["status"]
    if status == "archived":
        return include_archived
    return status in {"published", "scheduled"} and parse_date(publication.get("publishedAt")) <= now


def category_memberships(publication, categories):
    result=set()
    for identity in [publication['primaryCategory'],*publication.get('secondaryCategories',[])]:
        while identity and identity not in result:
            result.add(identity)
            identity=categories.get(identity,{}).get('parentId')
    return result
