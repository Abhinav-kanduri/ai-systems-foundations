import unittest
from examples.mini_world_model import predict_next_state, choose_action, run_deterministic, run_noisy

class MiniWorldTests(unittest.TestCase):
    def test_transition(self): self.assertEqual(predict_next_state(2, 1), 3)
    def test_action_bound(self): self.assertEqual(choose_action(0, 5), 1)
    def test_goal(self): self.assertEqual(run_deterministic(), 5)
    def test_noisy_safe(self): self.assertTrue(-1 <= run_noisy(.15, seed=11) <= 6)

if __name__ == '__main__': unittest.main()
