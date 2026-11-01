import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from coordination_simulator import Metrics, feasible, deterministic_baseline, coordinator

class TestCoordinator(unittest.TestCase):
    def test_baseline_feasible(self):
        m=Metrics()
        self.assertTrue(feasible(m,deterministic_baseline(m)))
    def test_stale_revision_rejected(self):
        m=Metrics()
        self.assertFalse(coordinator(m,{'cost':70},expected_revision=41)['approved'])
    def test_selected_candidate_feasible(self):
        m=Metrics()
        decision=coordinator(m,{'cost':70,'performance':115,'reliability':100},42)
        self.assertTrue(decision['approved'])
        self.assertTrue(feasible(m,decision['candidate']))
    def test_impossible_budget(self):
        m=Metrics(gpu_budget_hourly=2)
        self.assertIsNone(deterministic_baseline(m))
        self.assertFalse(coordinator(m,{'cost':70},42)['approved'])

if __name__ == '__main__': unittest.main()
