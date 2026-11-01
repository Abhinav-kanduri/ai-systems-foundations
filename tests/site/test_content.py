import json
import shutil
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from publication_content import load_library, render_markdown, split_frontmatter
from publication_model import PublicationError


class ContentTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(ROOT / "content", self.root / "content")
        self.now = datetime(2026, 10, 31, 23, tzinfo=timezone.utc)

    def article(self, slug="fixture", status="published", **extra):
        folder = self.root / "content/articles" / slug
        folder.mkdir(parents=True, exist_ok=True)
        metadata = {"id": slug, "title": "TEST FIXTURE " + slug, "summary": "Fixture only", "primaryCategory": "gpu", "publicationType": "technical-article", "status": status, "publishedAt": "2026-10-30", **extra}
        (folder / "README.md").write_text("---\n" + json.dumps(metadata) + "\n---\n# Fixture\n\nA searchable tensor-memory phrase.\n", encoding="utf-8")
        return folder

    def test_real_source_loader(self):
        library = load_library(self.root, self.now)
        self.assertEqual(len(library["publications"]), 1)
        self.assertEqual(library["publications"][0]["id"], "fde-field-guide")
        self.assertGreater(len(library["publications"][0]["tableOfContents"]), 100)

    def test_new_article_discovered_without_code_changes(self):
        self.article()
        library = load_library(self.root, self.now)
        self.assertEqual(len(library["publications"]), 2)
        fixture = next(p for p in library["publications"] if p["id"] == "fixture")
        self.assertIn("tensor-memory", fixture["searchText"])
        self.assertEqual(fixture["slug"], "test-fixture-fixture")

    def test_draft_review_future_excluded(self):
        for status in ("draft", "review"):
            self.article(status, status)
        self.article("future", "scheduled", publishedAt="2026-11-02T10:00:00-07:00")
        library = load_library(self.root, self.now)
        self.assertEqual([p["id"] for p in library["routes"]], ["fde-field-guide"])
        later = load_library(self.root, datetime(2026, 11, 3, tzinfo=timezone.utc))
        self.assertIn("future", [p["id"] for p in later["publications"]])

    def test_archived_retains_route_without_discovery(self):
        self.article(status="archived")
        library = load_library(self.root, self.now)
        self.assertEqual(len(library["publications"]), 1)
        self.assertEqual(len(library["routes"]), 2)

    def test_invalid_yaml_and_duplicate_keys(self):
        with self.assertRaises(PublicationError):
            split_frontmatter("---\ntitle: one\ntitle: two\n---\nBody")

    def test_rendering_and_security(self):
        value = '# Hello\n\n## Same\n\n## Same\n\n```python\nprint(1)\n```\n\n| A | B |\n|---|---|\n| 1 | 2 |\n\nInline $x^2$ and [reference](https://example.org).\n\n<img src="x" onerror="alert(1)"><script>alert(1)</script>\n\n[unsafe](javascript:alert(1))'
        html, toc = render_markdown(value)
        self.assertIn('class="codehilite"', html)
        self.assertIn('<table>', html)
        self.assertIn('<math', html)
        self.assertIn('loading="lazy"', html)
        self.assertNotIn('onerror', html)
        self.assertNotIn('<script', html)
        self.assertNotIn('javascript:', html)
        self.assertEqual(len({t["id"] for t in toc}), len(toc))

    def test_code_does_not_become_math(self):
        rendered, _ = render_markdown('```python\nprice = "$not_math$"\n```\n')
        self.assertNotIn('<math', rendered)


if __name__ == "__main__":
    unittest.main()
