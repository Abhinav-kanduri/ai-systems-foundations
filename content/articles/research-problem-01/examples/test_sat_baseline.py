import unittest
from sat_baseline import evaluate_formula, find_witness

class SatBaselineTests(unittest.TestCase):
    def test_example_witness(self):
        self.assertTrue(evaluate_formula(True, False, True))
    def test_known_false_case(self):
        self.assertFalse(evaluate_formula(False, False, False))
    def test_witness_is_valid(self):
        self.assertTrue(evaluate_formula(*find_witness()))

if __name__ == '__main__':
    unittest.main()
