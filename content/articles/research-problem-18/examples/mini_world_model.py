"""Research Problem 18: tiny CPU-only dynamics + closed-loop feedback demo."""
import argparse
import random


def predict_next_state(position: float, action: float) -> float:
    """A deterministic model, not a trained neural world model."""
    return position + action


def choose_action(position: float, target: float, max_step: float = 1.0) -> float:
    remaining = target - position
    return max(-max_step, min(max_step, remaining))


def run_deterministic():
    position, target, safe_min, safe_max = 0.0, 5.0, -1.0, 6.0
    for step in range(10):
        action = choose_action(position, target)
        predicted = predict_next_state(position, action)
        if not safe_min <= predicted <= safe_max:
            print('Unsafe predicted action. Stopping.')
            break
        observed = predicted  # no disturbance in the basic model
        print(f'Step {step}: action={action:.1f}, predicted={predicted:.1f}, observed={observed:.1f}')
        position = observed
        if abs(position - target) < 1e-9:
            print('Target reached.')
            break
    return position


def run_noisy(noise: float, seed: int = 11):
    """Feedback-based replanning with a toy bounded disturbance.

    Real motion requires an independent safety supervisor; this is illustrative only.
    """
    rng = random.Random(seed)
    position, target, safe_min, safe_max = 0.0, 5.0, -1.0, 6.0
    for step in range(20):
        action = choose_action(position, target)
        predicted = predict_next_state(position, action)
        # Robustly enforce the NEXT position against the entire bounded noise interval.
        if predicted - noise < safe_min or predicted + noise > safe_max:
            print('Safety uncertainty bound exceeded. Stopping.')
            break
        observed = predicted + rng.uniform(-noise, noise)
        print(f'Step {step:02d}: predicted={predicted:.3f}, observed={observed:.3f}, error={observed-predicted:+.3f}')
        position = observed  # replan after every observation
        if abs(position - target) < max(0.1, noise):
            print('Near target.')
            break
    return position


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--noise', type=float, default=0.0, help='Maximum magnitude of uniform movement disturbance')
    parser.add_argument('--seed', type=int, default=11)
    args = parser.parse_args()
    if args.noise < 0:
        parser.error('--noise must be nonnegative')
    run_deterministic() if args.noise == 0 else run_noisy(args.noise, args.seed)
