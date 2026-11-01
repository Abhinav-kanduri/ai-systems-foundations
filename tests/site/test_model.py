import copy
import json
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from publication_model import PublicationError, publicly_available, validate_metadata, validate_relationships, validate_taxonomy


class ModelTests(unittest.TestCase):
    def setUp(self):
        self.schema = json.loads((ROOT / "content/publication.schema.json").read_text(encoding='utf-8'))
        self.taxonomy = json.loads((ROOT / "content/taxonomy.json").read_text(encoding='utf-8'))
        self.categories = {x["id"] for x in self.taxonomy["categories"]}
        self.types = {x["id"] for x in self.taxonomy["publicationTypes"]}
        self.meta = json.loads((ROOT / "content/guides/end-to-end-fde-learning-map/publication.json").read_text(encoding='utf-8'))

    def validate(self, meta=None):
        return validate_metadata(meta or self.meta, self.schema, self.categories, self.types)

    def test_real_metadata(self):
        validate_taxonomy(self.taxonomy)
        self.assertEqual(self.validate()["id"], "fde-field-guide")

    def test_required_date(self):
        del self.meta["publishedAt"]
        with self.assertRaisesRegex(PublicationError, "publishedAt"):
            self.validate()

    def test_invalid_date(self):
        self.meta["publishedAt"] = "2026-02-30"
        with self.assertRaisesRegex(PublicationError, "real ISO date"):
            self.validate()

    def test_category_and_type(self):
        for field in ("primaryCategory", "publicationType"):
            meta = dict(self.meta, **{field: "missing"})
            with self.assertRaises(PublicationError):
                self.validate(meta)

    def test_slug_default_and_reserved(self):
        del self.meta["slug"]
        self.assertEqual(self.validate()["slug"], "end-to-end-fde-learning-map")
        self.meta["slug"] = "topics"
        with self.assertRaisesRegex(PublicationError, "reserved"):
            self.validate()

    def test_duplicate_slug_and_id(self):
        p = self.validate()
        with self.assertRaisesRegex(PublicationError, "duplicate publication"):
            validate_relationships([p, p], {})
        q = dict(p, id="other")
        with self.assertRaisesRegex(PublicationError, "duplicate publication slug"):
            validate_relationships([p, q], {})

    def test_missing_and_self_related(self):
        for value in ("missing", self.meta["id"]):
            p = dict(self.validate(), relatedPublicationIds=[value])
            with self.assertRaisesRegex(PublicationError, "related"):
                validate_relationships([p], {})

    def test_series_order_and_missing_references(self):
        p = dict(self.validate(), seriesId="series", seriesOrder=2)
        c = {"id": "series", "slug": "series", "title": "Series", "description": "Test", "publicationIds": [p["id"]]}
        with self.assertRaisesRegex(PublicationError, "seriesOrder"):
            validate_relationships([p], {"series": [c]})
        c["publicationIds"] = ["missing"]
        with self.assertRaisesRegex(PublicationError, "unknown publication"):
            validate_relationships([p], {"series": [c]})

    def test_draft_review_schedule(self):
        now = datetime(2026, 10, 31, tzinfo=timezone.utc)
        for status in ("draft", "review"):
            self.assertFalse(publicly_available(dict(self.meta, status=status), now))
        scheduled = dict(self.meta, status="scheduled", publishedAt="2026-11-01T08:00:00-07:00")
        self.validate(scheduled)
        self.assertFalse(publicly_available(scheduled, now))
        self.assertTrue(publicly_available(scheduled, datetime(2026, 11, 2, tzinfo=timezone.utc)))
        self.assertFalse(publicly_available(dict(self.meta, status="archived"), now))

    def test_url_lock(self):
        p = self.validate()
        registry = {p["id"]: {"slug": "previous", "canonicalUrl": "https://example.org/previous/"}}
        with self.assertRaisesRegex(PublicationError, "locked"):
            validate_relationships([p], {}, registry)

    def test_taxonomy_cycles(self):
        t = copy.deepcopy(self.taxonomy)
        t["categories"][0]["parentId"] = t["categories"][0]["id"]
        with self.assertRaisesRegex(PublicationError, "circular"):
            validate_taxonomy(t)


if __name__ == "__main__":
    unittest.main()
