import hashlib
import json
import re
import sys
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from publication_content import load_library, render_markdown, plain_text
from publication_model import PublicationError
from research_learning import validate_learning, safe_svg


class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.ids=set()
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if attrs.get('id'): self.ids.add(attrs['id'])
        if tag in {'a','img','script','link'}:
            value=attrs.get('href') or attrs.get('src')
            if value: self.links.append(value)


class ResearchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.library=load_library(ROOT)
        cls.articles=[p for p in cls.library['publications'] if p.get('problemNumber')]
        cls.manifest=json.loads((ROOT/'docs/research-publications/source-manifest.json').read_text(encoding='utf-8'))

    def test_twenty_unique_entries_and_series(self):
        self.assertEqual(sorted(p['problemNumber'] for p in self.articles),list(range(1,21)))
        self.assertEqual(len({p['slug'] for p in self.articles}),20)
        series=next(c for c in self.library['collections']['series'] if c['id']=='research-to-reality')
        self.assertEqual(series['publicationIds'],[f'research-problem-{n:02}' for n in range(1,21)])
        self.assertIn('fde-field-guide',[p['id'] for p in self.library['publications']])

    def test_source_bodies_and_every_supporting_file_preserved(self):
        for item in self.manifest['articles']:
            for file in item['files']:
                path=ROOT/file['path']
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),file['sha256'],str(path))
            self.assertTrue(item['elements']['sections'])
            self.assertTrue(item['elements']['mermaidBlocks'])

    def test_full_code_and_diagram_sources_in_rendered_articles(self):
        for p in self.articles:
            # Include entire code bodies, not just their counts or headings.
            text=plain_text(p['html'])
            for language, code in re.findall(r'(?ms)^```([^\n]*)\n(.*?)^```\s*$',p['body']):
                normalized=''.join(code.split())
                self.assertIn(normalized,''.join(text.split()),(p['id'],language,code[:70]))
            for uri in re.findall(r'\]\((https?://[^)]+)\)',p['body']):
                self.assertIn(uri.replace('&','&amp;'),p['html'],p['id'])

    def test_source_sections_and_tables_have_rendered_content(self):
        for p in self.articles:
            self.assertTrue(re.search(r'problem statement',p['html'],re.I),p['id'])
            self.assertIn('<table>',p['html'],p['id'])
            self.assertTrue(re.search(r'interview perspective',p['html'],re.I),p['id'])
            self.assertTrue(re.search(r'takeaway',p['html'],re.I),p['id'])

    def test_math_delimiters_and_source_preservation(self):
        for source in [r'Inline \(x^2+y^2\)', '\\[\nx^2 + y^2\n\\]', 'Inline $x_1$']:
            rendered,_=render_markdown(source)
            self.assertIn('<math',rendered)
            self.assertIn('application/x-tex',rendered)
        rendered,_=render_markdown('```python\ntext = "\\\\(not math\\\\)"\n```')
        self.assertNotIn('<math',rendered)

    def test_invalid_quiz_and_untrusted_diagram_content(self):
        value=dict(self.articles[0]['learning'])
        value['quiz']={'question':'Question','choices':['A','B'],'answer':9,'explanation':'Explain'}
        with self.assertRaises(PublicationError):validate_learning(value)
        rendered,_=render_markdown('```mermaid\nflowchart LR\n A[<script>alert(1)</script>] --> B\n```')
        self.assertNotIn('<script>',rendered)
        data=safe_svg(b'<svg xmlns="http://www.w3.org/2000/svg"><script>alert(1)</script><image href="https://example.org/pixel" onload="alert(1)"/></svg>')
        self.assertNotIn(b'<script',data);self.assertNotIn(b'onload',data);self.assertNotIn(b'https://',data)


if __name__=='__main__':unittest.main()
