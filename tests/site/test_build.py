import hashlib
import json
import shutil
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote,urlsplit

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
from build_publications import build
from publication_model import PublicationError
from fixture_content import copy_fixture_content


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__();self.links=[]
    def handle_starttag(self,tag,attributes):
        attributes=dict(attributes)
        if tag in {'a','link','img','script'}:
            value=attributes.get('href') or attributes.get('src')
            if value:self.links.append(value)


class BuildTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        for folder in ('content','docs','assets'):
            if folder == 'content':
                copy_fixture_content(self.root/folder)
            else:
                shutil.copytree(ROOT/folder,self.root/folder)
        self.now=datetime(2026,10,31,23,tzinfo=timezone.utc)
        self.output=self.root/'build/site'

    def article(self,identity,status='published',**extra):
        folder=self.root/'content/articles'/identity;folder.mkdir(parents=True,exist_ok=True)
        meta={'id':identity,'slug':identity,'title':'TEST FIXTURE '+identity,'summary':'Fixture only','primaryCategory':'gpu','publicationType':'technical-article','status':status,'publishedAt':'2026-10-30',**extra}
        (folder/'README.md').write_text('---\n'+json.dumps(meta)+'\n---\n# Fixture\n\n## Memory hierarchy\n\nFixture tensor-memory phrase.\n',encoding='utf-8')
        return folder

    def run_build(self):
        return build(self.root,self.output,self.now)

    def test_new_article_routes_indexes_and_counts(self):
        self.article('new-article')
        self.run_build()
        self.assertTrue((self.output/'publications/new-article/index.html').is_file())
        data=json.loads((self.output/'publications/index.json').read_text(encoding='utf-8'))
        self.assertEqual(len(data['publications']),2)
        self.assertIn('Memory hierarchy',(self.output/'publications/new-article/index.html').read_text(encoding='utf-8'))
        self.assertIn('new-article',(self.output/'publications/topics/gpu-and-accelerator-architecture/index.html').read_text(encoding='utf-8'))

    def test_drafts_future_and_related_metadata_do_not_leak(self):
        self.article('private-draft','draft')
        self.article('private-review','review')
        self.article('private-future','scheduled',publishedAt='2027-01-01T10:00:00Z')
        self.article('public',relatedPublicationIds=['private-draft'])
        self.run_build()
        for path in self.output.rglob('*'):
            if path.is_file() and path.suffix in {'.html','.json','.xml'}:
                text=path.read_text(encoding='utf-8')
                self.assertNotIn('private-draft',text,path)
                self.assertNotIn('private-review',text,path)
                self.assertNotIn('private-future',text,path)
        self.assertFalse((self.output/'content/articles').exists())

    def test_rebuild_removes_stale_published_route(self):
        self.article('transition');self.run_build()
        self.assertTrue((self.output/'publications/transition').exists())
        self.article('transition','draft');self.run_build()
        self.assertFalse((self.output/'publications/transition').exists())

    def test_failed_build_preserves_last_good_artifact(self):
        self.run_build();before=(self.output/'publications/index.json').read_bytes()
        self.article('invalid',primaryCategory='missing')
        with self.assertRaises(PublicationError):self.run_build()
        self.assertEqual((self.output/'publications/index.json').read_bytes(),before)

    def test_archive_route_retained_without_feed_or_search(self):
        self.article('retired','archived');self.run_build()
        self.assertIn('Archived publication',(self.output/'publications/retired/index.html').read_text(encoding='utf-8'))
        for name in ('publications/index.json','publications/feed.xml','sitemap.xml'):
            self.assertNotIn('retired',(self.output/name).read_text(encoding='utf-8'))

    def test_real_artifact_links_resolve(self):
        self.run_build()
        for path in self.output.rglob('*.html'):
            parser=LinkParser();parser.feed(path.read_text(encoding='utf-8'))
            for value in parser.links:
                parsed=urlsplit(value)
                if parsed.scheme or not parsed.path:continue
                target=(path.parent/unquote(parsed.path)).resolve()
                self.assertTrue(target.is_relative_to(self.output))
                self.assertTrue(target.exists(),(path,value))

    def test_feed_and_sitemap_and_fde_integrity(self):
        self.run_build()
        feed=ET.parse(self.output/'publications/feed.xml')
        self.assertEqual(len(feed.findall('./channel/item')),1)
        ET.parse(self.output/'sitemap.xml')
        source=self.root/'content/guides/end-to-end-fde-learning-map/README.md'
        self.assertEqual(source.read_bytes(),(self.output/'content/fde-learning-map.md').read_bytes())
        baseline=json.loads((ROOT/'reports/publications/baseline.json').read_text(encoding='utf-8'))
        self.assertEqual(hashlib.sha256(source.read_bytes().replace(b'\r\n',b'\n')).hexdigest(),baseline['fdeNormalizedSha256'])

    def test_preview_is_separate_and_noindex(self):
        self.article('private-draft','draft')
        build(self.root,self.root/'build/preview',self.now,preview_id='private-draft')
        page=self.root/'build/preview/publications/private-draft/index.html'
        self.assertIn('PRIVATE PREVIEW',page.read_text(encoding='utf-8'))
        self.assertIn('noindex,nofollow',page.read_text(encoding='utf-8'))
        self.run_build()
        self.assertFalse((self.output/'publications/private-draft').exists())

    def test_output_cannot_overwrite_source(self):
        with self.assertRaises(PublicationError):build(self.root,self.root/'content',self.now)


if __name__=='__main__':unittest.main()
