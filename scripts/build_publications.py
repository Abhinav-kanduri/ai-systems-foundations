"""Build only distributable website files; drafts never enter the public output."""
from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
import uuid
import xml.etree.ElementTree as ET
from email.utils import format_datetime
from datetime import datetime, timezone
from pathlib import Path
from pygments.formatters import HtmlFormatter

from publication_content import load_library, public_record, render_markdown
from publication_model import PublicationError, parse_date
from publication_views import about_page, article_page, author_banner, editorial_note, index_page

ROOT = Path(__file__).resolve().parents[1]


def write_page(output, route, value):
    folder = output / route
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "index.html").write_text(value, encoding="utf-8")


def render_artifact(root, output, now=None, preview_id=None):
    root = Path(root).resolve()
    output = Path(output or root / "build/site").resolve()
    # Never erase a caller-supplied directory: only our generated files are replaced.
    if output == root or output.is_relative_to(root / "content") or output.is_relative_to(root / "docs"):
        raise PublicationError("output must be separate from source content and docs")
    library = load_library(root, now)
    if preview_id:
        preview = next((p for p in library['records'] if p['id'] == preview_id), None)
        if not preview:
            raise PublicationError(f"unknown preview publication '{preview_id}'")
        library['routes'] = [p for p in library['routes'] if p['id'] != preview_id] + [preview]
    output.mkdir(parents=True, exist_ok=True)
    assets = output / "assets"
    assets.mkdir(exist_ok=True)
    for path in (root / "docs/assets").iterdir():
        if path.is_file():
            shutil.copy2(path, assets / path.name)
    if (root / 'docs/assets/vendor').exists():
        shutil.copytree(root / 'docs/assets/vendor', assets / 'vendor')
    banner=library['site'].get('authorBanner')
    if banner:
        relative=Path(banner['src'])
        source=(root/relative).resolve()
        if relative.is_absolute() or not source.is_relative_to((root/'assets').resolve()) or not source.is_file():
            raise PublicationError('authorBanner.src must reference an existing file inside assets/')
        target=output/relative
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(source,target)
    (assets / 'code.css').write_text(HtmlFormatter(style='github-dark').get_style_defs('.codehilite'),encoding='utf-8')
    fde_page = (root / 'docs/index.html').read_text(encoding='utf-8')
    fde_page=fde_page.replace('</head>','<link rel="stylesheet" href="assets/resources.css">\n</head>')
    footer='<div class="fde-author-banner">'+author_banner(library,'',lazy=True)+editorial_note(library)+'</div>'
    fde_page=fde_page.replace('<footer class="site-footer">',footer+'\n<footer class="site-footer">')
    fde_metadata = '<link rel="canonical" href="' + library['site']['siteUrl'] + '"><meta property="og:title" content="FDE Field Guide"><meta property="og:image" content="' + library['site']['siteUrl'] + 'assets/publications-social.png">'
    (output / 'index.html').write_text(fde_page.replace('</head>',fde_metadata + '\n</head>'),encoding='utf-8')
    shutil.copy2(root / "docs/.nojekyll", output / ".nojekyll")
    content = output / "content"
    content.mkdir(exist_ok=True)
    shutil.copy2(root / "content/guides/end-to-end-fde-learning-map/README.md", content / "fde-learning-map.md")
    about_source = root / 'content/about.md'
    if about_source.exists():
        rendered, _ = render_markdown(about_source.read_text(encoding='utf-8'))
        write_page(output, 'publications/about/', about_page(library, rendered))
    for kind in ("overview", "latest", "topics", "series", "paths"):
        route = "publications/" if kind == "overview" else f"publications/{kind}/"
        write_page(output, route, index_page(library, route, kind))
    for category in library["taxonomy"]["categories"]:
        route = f"publications/topics/{category['slug']}/"
        write_page(output, route, index_page(library, route, "topics", category=category))
    for kind, collections in library["collections"].items():
        for collection in collections:
            route = f"publications/{kind}/{collection['slug']}/"
            write_page(output, route, index_page(library, route, kind, collection=collection))
    for publication in library['routes']:
        route = f"publications/{publication['slug']}/"
        write_page(output, route, article_page(library,publication,route,preview=publication['id']==preview_id))
        copy_publication_assets(root,output,route,publication)
    visible_ids = {p["id"] for p in library["publications"]}
    records = []
    for p in library["publications"]:
        record = public_record(p)
        record['relatedPublicationIds'] = [i for i in record.get('relatedPublicationIds', []) if i in visible_ids]
        if record.get('seriesId') not in {c['id'] for c in library['collections']['series']}:
            record.pop('seriesId',None)
            record.pop('seriesOrder',None)
        records.append(record)
    manifest = {"publications": records, "taxonomy": library["taxonomy"], "collections": library["collections"]}
    (output / "publications/index.json").write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
    generate_feeds(output,library)
    if preview_id:
        for path in output.rglob('*.html'):
            value = path.read_text(encoding='utf-8').replace('</head>','<meta name="robots" content="noindex,nofollow">\n</head>')
            path.write_text(value,encoding='utf-8')
    generated = sorted(p.relative_to(output).as_posix() for p in output.rglob('*') if p.is_file())
    (output / 'build-manifest.json').write_text(json.dumps({'publications':[p['id'] for p in library['publications']],'files':generated},indent=2),encoding='utf-8')
    return library


def copy_publication_assets(root, output, route, publication):
    allowed = {'.png','.jpg','.jpeg','.webp','.avif','.gif','.svg','.pdf','.txt','.csv','.ipynb','.py','.json'}
    folder = (root / publication['source']).parent
    if publication.get('packageFiles'):
        paths = []
        for name in publication['packageFiles']:
            path = (folder / name).resolve()
            if not path.is_relative_to(folder.resolve()) or not path.is_file():
                raise PublicationError(f'Invalid research package file: {name}')
            paths.append(path)
        copy_research_files(folder, output / route, paths)
        return
    for name in ('assets','examples'):
        source = folder / name
        if not source.exists():
            continue
        for path in source.rglob('*'):
            if not path.is_file() or path.suffix.lower() not in allowed:
                continue
            if not path.resolve().is_relative_to(folder.resolve()):
                raise PublicationError(f"asset escapes publication folder: {path}")
            target = output / route / name / path.relative_to(source)
            target.parent.mkdir(parents=True,exist_ok=True)
            if path.suffix.lower() == '.svg':
                # SVG assets may be opened directly: remove active content too.
                tree = ET.fromstring(path.read_bytes())
                for parent in tree.iter():
                    for child in list(parent):
                        if child.tag.split('}')[-1] in {'script','foreignObject','iframe'}:
                            parent.remove(child)
                    for key,value in list(parent.attrib.items()):
                        if key.split('}')[-1].lower().startswith('on') or (key.split('}')[-1] in {'href','src'} and value.lstrip().lower().startswith(('javascript:','data:'))):
                            del parent.attrib[key]
                target.write_bytes(ET.tostring(tree))
            else:
                shutil.copy2(path,target)


def copy_research_files(folder, destination, paths):
    """Publish the inventoried package, keeping executable HTML as plain text."""
    from research_learning import safe_svg
    directories = {destination}
    for path in paths:
        relative = path.relative_to(folder.resolve())
        target = destination / relative
        if path.suffix.lower() in {'.html', '.htm', '.js'}:
            target = target.with_name(target.name + '.txt')
        target.parent.mkdir(parents=True, exist_ok=True)
        directories.add(target.parent)
        if path.suffix.lower() == '.svg':
            target.write_bytes(safe_svg(path.read_bytes()))
        else:
            shutil.copy2(path, target)
    # Explicit, generated file indexes support original links such as diagrams/.
    for directory in sorted(directories, key=lambda p: len(p.parts), reverse=True):
        if directory == destination:
            continue
        import html
        links = ''.join('<li><a href="' + html.escape(p.name + ('/' if p.is_dir() else ''), quote=True) + '">' + html.escape(p.name) + '</a></li>' for p in sorted(directory.iterdir()) if p.name != 'index.html')
        (directory / 'index.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Source package files</title><h1>Source package files</h1><p><a href="../">Back</a></p><ul>' + links + '</ul></html>', encoding='utf-8')


def generate_feeds(output,library):
    site = library['site']
    rss = ET.Element('rss',version='2.0')
    channel = ET.SubElement(rss,'channel')
    for key,value in [('title',site['title']),('link',site['siteUrl']+'publications/'),('description',site['description']),('language','en')]:
        ET.SubElement(channel,key).text = value
    for publication in library['publications']:
        item = ET.SubElement(channel,'item')
        for key,value in [('title',publication['title']),('link',publication['canonicalUrl']),('description',publication['summary']),('pubDate',format_datetime(parse_date(publication['publishedAt'])))]:
            ET.SubElement(item,key).text = value
        ET.SubElement(item,'guid',isPermaLink='true').text = publication['canonicalUrl']
    ET.ElementTree(rss).write(output/'publications/feed.xml',encoding='utf-8',xml_declaration=True)
    urls = {site['siteUrl']}
    for path in (output/'publications').rglob('index.html'):
        route = path.parent.relative_to(output).as_posix()+'/'
        if any(route == f"publications/{p['slug']}/" for p in library['routes']):
            continue
        urls.add(site['siteUrl']+route)
    urls.update(p['canonicalUrl'] for p in library['publications'] if p['canonicalUrl'].startswith(site['siteUrl']))
    sitemap = ET.Element('urlset',xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
    for url in sorted(urls):
        entry = ET.SubElement(sitemap,'url'); ET.SubElement(entry,'loc').text=url
        publication = next((p for p in library['publications'] if p['canonicalUrl']==url),None)
        if publication:
            ET.SubElement(entry,'lastmod').text=(publication.get('updatedAt') or publication['publishedAt'])[:10]
    ET.ElementTree(sitemap).write(output/'sitemap.xml',encoding='utf-8',xml_declaration=True)
    (output/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+site['siteUrl']+'sitemap.xml\n',encoding='utf-8')


def build(root=ROOT,output=None,now=None,preview_id=None):
    root=Path(root).resolve()
    build_root=root/'build'
    output=Path(output or build_root/'site').resolve()
    if not output.is_relative_to(build_root.resolve()) or output==build_root.resolve():
        raise PublicationError('output must be a generated directory inside this repository’s build/ folder')
    build_root.mkdir(exist_ok=True)
    staging=Path(tempfile.mkdtemp(prefix='.publications-',dir=build_root)).resolve()
    backup=build_root/('.previous-'+uuid.uuid4().hex)
    try:
        library=render_artifact(root,staging,now,preview_id)
        output.parent.mkdir(parents=True,exist_ok=True)
        if output.exists():
            output.rename(backup)
        try:
            staging.rename(output)
        except OSError:
            if backup.exists():
                backup.rename(output)
            raise
        if backup.exists():
            assert backup.resolve().is_relative_to(build_root.resolve())
            shutil.rmtree(backup)
        return library
    finally:
        if staging.exists():
            assert staging.resolve().is_relative_to(build_root.resolve())
            shutil.rmtree(staging)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--now", help="Timezone-qualified build timestamp, useful for scheduled-content checks")
    args = parser.parse_args()
    try:
        now = datetime.fromisoformat(args.now.replace("Z", "+00:00")) if args.now else None
        library = build(output=args.output, now=now)
        print(f"Built {len(library['publications'])} public publication(s) into {args.output or ROOT / 'build/site'}")
    except (PublicationError, ValueError) as error:
        print(f"Publication build failed:\n{error}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
