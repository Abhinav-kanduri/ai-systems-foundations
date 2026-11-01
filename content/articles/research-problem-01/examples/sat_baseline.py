"""Brute-force Boolean SAT learning baseline. Standard library only."""
import argparse
from itertools import product


def evaluate_formula(x1: bool, x2: bool, x3: bool) -> bool:
    """(x1 OR x2) AND (NOT x1 OR x3)."""
    return (x1 or x2) and ((not x1) or x3)


def find_witness():
    for values in product((False, True), repeat=3):
        if evaluate_formula(*values):
            return values
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--variables', type=int, default=3)
    parser.add_argument('--count-only', action='store_true')
    args = parser.parse_args()
    if args.variables < 0:
        parser.error('--variables must be non-negative')
    print(f'{args.variables} variables -> {2 ** args.variables:,} Boolean assignments')
    if args.count_only:
        return
    if args.variables != 3:
        parser.error('the implemented formula has exactly 3 variables; use --count-only otherwise')
    witness = find_witness()
    print('Satisfying assignment:', dict(zip(('x1', 'x2', 'x3'), witness)) if witness else None)


if __name__ == '__main__':
    main()
