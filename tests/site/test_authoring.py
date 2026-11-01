import contextlib
import io
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
import publications as commands
from publication_content import load_library,split_frontmatter
from publication_model import PublicationError


class AuthoringTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        shutil.copytree(ROOT/'content',self.root/'content')
        self.patch=patch.object(commands,'ROOT',self.root);self.patch.start();self.addCleanup(self.patch.stop)
        self.stdout=contextlib.redirect_stdout(io.StringIO());self.stdout.__enter__();self.addCleanup(lambda:self.stdout.__exit__(None,None,None))

    def test_new_publish_and_url_registration(self):
        commands.create('TEST FIXTURE GPU','gpu','technical-article')
        source=self.root/'content/articles/test-fixture-gpu/README.md'
        metadata,_=split_frontmatter(source.read_text(encoding='utf-8'))
        self.assertEqual(metadata['status'],'draft')
        self.assertEqual(len(load_library(self.root)['publications']),1)
        commands.publish(metadata['id'],'2026-10-30')
        metadata,_=split_frontmatter(source.read_text(encoding='utf-8'))
        self.assertEqual(metadata['status'],'published')
        registry=json.loads((self.root/'content/url-registry.json').read_text(encoding='utf-8'))
        self.assertIn(metadata['id'],registry)
        with self.assertRaisesRegex(PublicationError,'Original publication date'):
            commands.publish(metadata['id'],'2026-10-29')

    def test_invalid_category_writes_no_source(self):
        with self.assertRaises(PublicationError):commands.create('TEST FIXTURE INVALID','missing','technical-article')
        self.assertFalse((self.root/'content/articles/test-fixture-invalid').exists())

    def test_scheduled_and_review_lifecycle(self):
        commands.create('TEST FIXTURE FUTURE','gpu','technical-article')
        commands.publish('test-fixture-future','2099-01-01T09:00:00-07:00')
        library=load_library(self.root)
        self.assertEqual(len(library['publications']),1)
        self.assertEqual(next(p for p in library['records'] if p['slug']=='test-fixture-future')['status'],'scheduled')


if __name__=='__main__':unittest.main()
