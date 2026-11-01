"""Authoring commands: new, validate, publish, build, serve, and private preview."""
from __future__ import annotations

import argparse
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

import yaml

from build_publications import ROOT, build
from publication_content import load_library, split_frontmatter
from publication_model import PublicationError, parse_date, slugify


def create(title, category, publication_type):
    library=load_library(ROOT)
    slug=slugify(title)
    if not slug or slug in {p['slug'] for p in library['records']}:
        raise PublicationError('Choose a nonempty, unique title/slug')
    metadata={'id':'pub-'+uuid.uuid4().hex[:12],'slug':slug,'title':title,'summary':'Add a concise summary before publication.','author':library['site'].get('defaultAuthor'),'primaryCategory':category,'publicationType':publication_type,'status':'draft','publishedAt':None,'updatedAt':None,'tags':[],'relatedPublicationIds':[],'canonicalUrl':None}
    from publication_model import validate_metadata
    schema=json.loads((ROOT/'content/publication.schema.json').read_text(encoding='utf-8'))
    validate_metadata(metadata,schema,{c['id'] for c in library['taxonomy']['categories']},{t['id'] for t in library['taxonomy']['publicationTypes']})
    folder=ROOT/'content/articles'/slug
    if folder.exists():
        raise PublicationError(f'Folder already exists: {folder}')
    folder.mkdir(parents=True)
    template=(ROOT/'content/templates/article.md').read_text(encoding='utf-8')
    _,body=split_frontmatter(template)
    body=body.replace('# Your article title','# '+title,1)
    source=folder/'README.md'
    source.write_text('---\n'+yaml.safe_dump(metadata,sort_keys=False,allow_unicode=True)+'---\n'+body,encoding='utf-8')
    print(f'Created draft {metadata["id"]}: {source.relative_to(ROOT)}')
    print('Edit the content and metadata, then preview it before publishing.')


def publish(identity,when):
    library=load_library(ROOT)
    p=next((p for p in library['records'] if identity in {p['id'],p['slug']}),None)
    if not p:
        raise PublicationError('Unknown publication id or slug')
    when_parsed=parse_date(when)
    if not when_parsed:
        raise PublicationError('Supply the original publication date or intended publication timestamp')
    source=ROOT/p['source'];original=source.read_text(encoding='utf-8')
    metadata,body=split_frontmatter(original)
    target=source.with_name('publication.json') if metadata is None else source
    target_original=target.read_text(encoding='utf-8')
    if metadata is None:
        metadata=json.loads(target_original)
    if metadata.get('publishedAt') and metadata['publishedAt'] != when and metadata.get('status') in {'published','archived'}:
        raise PublicationError('Original publication date is already set; use updatedAt for revisions')
    scheduled=when_parsed>datetime.now(timezone.utc)
    metadata['publishedAt']=when
    metadata['status']='scheduled' if scheduled else 'published'
    if scheduled and 'T' not in when:
        raise PublicationError('Scheduled publishing requires a full timestamp with timezone')
    try:
        target.write_text(json.dumps(metadata,indent=2)+'\n' if target.suffix=='.json' else '---\n'+yaml.safe_dump(metadata,sort_keys=False,allow_unicode=True)+'---\n'+body,encoding='utf-8')
        validated=load_library(ROOT)
        final=next(item for item in validated['records'] if item['id']==p['id'])
        registry_path=ROOT/'content/url-registry.json'
        registry=json.loads(registry_path.read_text(encoding='utf-8'))
        registry.setdefault(p['id'],{'slug':final['slug'],'canonicalUrl':final['canonicalUrl']})
        registry_path.write_text(json.dumps(registry,indent=2)+'\n',encoding='utf-8')
    except Exception:
        target.write_text(target_original,encoding='utf-8')
        raise
    print(f'{p["id"]}: {metadata["status"]} at {when}. Content metadata updated; no deployment occurred.')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    commands=parser.add_subparsers(dest='command',required=True)
    new=commands.add_parser('new');new.add_argument('title');new.add_argument('--category',required=True);new.add_argument('--type',default='technical-article')
    commands.add_parser('validate');commands.add_parser('build')
    pub=commands.add_parser('publish');pub.add_argument('identity');pub.add_argument('--at',required=True)
    server=commands.add_parser('serve');server.add_argument('--port',type=int,default=8000)
    preview=commands.add_parser('preview');preview.add_argument('identity');preview.add_argument('--port',type=int,default=8002)
    args=parser.parse_args()
    try:
        if args.command=='new':
            create(args.title,args.category,args.type)
        elif args.command=='validate':
            library=load_library(ROOT); print(f'Validated {len(library["records"])} publication(s); {len(library["publications"])} currently public.')
        elif args.command=='publish':
            publish(args.identity,args.at)
        elif args.command=='build':
            library=build();print(f'Built {len(library["publications"])} public publication(s) into build/site.')
        else:
            from serve_site import serve
            if args.command=='preview':
                library=load_library(ROOT)
                p=next((p for p in library['records'] if args.identity in {p['id'],p['slug']}),None)
                if not p: raise PublicationError('Unknown preview publication')
                build(output=ROOT/'build/preview',preview_id=p['id'])
                print(f'Preview: http://localhost:{args.port}/publications/{p["slug"]}/',flush=True)
                serve(ROOT/'build/preview',args.port,watch=True,preview_id=p['id'])
            else:
                build();serve(ROOT/'build/site',args.port,watch=True)
    except (PublicationError,ValueError) as error:
        print(f'Publication command failed:\n{error}',file=sys.stderr);raise SystemExit(1)


if __name__=='__main__':
    main()
