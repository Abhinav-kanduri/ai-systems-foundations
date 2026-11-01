"""Educational example: float rounding differs from decimal financial rounding."""
from decimal import Decimal, ROUND_HALF_UP


def reference_interest(principal: str, rate: str) -> Decimal:
    """Declared reference policy: exact decimal math, ROUND_HALF_UP to cents."""
    amount = Decimal(principal) * Decimal(rate)
    return amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def naive_float_interest(principal: str, rate: str) -> float:
    """Deliberately problematic candidate: float + Python built-in round."""
    return round(float(principal) * float(rate), 2)


if __name__ == "__main__":
    for p, r in [("1.00", "0.125"), ("10.00", "0.0245"), ("100.00", "0.055")]:
        expected = reference_interest(p, r)
        observed = naive_float_interest(p, r)
        print(f"principal={p} rate={r} reference={expected} candidate={observed:.2f} match={expected == Decimal(str(observed))}")
