import unittest
from transfer_lab import transfer, guarded_transfer


class TransferLearningTests(unittest.TestCase):
    def test_standard_transfer(self):
        self.assertEqual(transfer(1000, 500, 200), (800, 700))

    def test_conservation_for_selected_inputs(self):
        for a, b, t in [(1000, 500, 200), (4, 6, -2), (0, 0, 900)]:
            x, y = transfer(a, b, t)
            self.assertEqual(x + y, a + b)

    def test_negative_transfer_rejected(self):
        with self.assertRaises(ValueError):
            guarded_transfer(1000, 500, -10, True)

    def test_insufficient_funds_rejected(self):
        with self.assertRaises(ValueError):
            guarded_transfer(1000, 500, 1200, True)

    def test_unauthorized_transfer_rejected(self):
        with self.assertRaises(PermissionError):
            guarded_transfer(1000, 500, 100, False)


if __name__ == '__main__':
    unittest.main()
