-- Research Problem 12: introductory proof exercise
-- Run with a compatible Lean 4 installation: lean ResearchProblem12.lean
theorem add_zero_example (n : Nat) : n + 0 = n := by
  simp

theorem succ_ne_zero_example (n : Nat) : Nat.succ n ≠ 0 := by
  simp
