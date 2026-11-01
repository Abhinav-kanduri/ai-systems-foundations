import sys
import unittest
from decimal import Decimal
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
from interest_migration import reference_interest, naive_float_interest

class InterestMigrationTests(unittest.TestCase):
    def test_decimal_half_up_tie(self):
        self.assertEqual(reference_interest("1.00", "0.125"), Decimal("0.13"))

    def test_candidate_disagreement_is_visible(self):
        expected = reference_interest("1.00", "0.125")
        candidate = Decimal(str(naive_float_interest("1.00", "0.125")))
        self.assertNotEqual(expected, candidate)

if __name__ == "__main__":
    unittest.main()
