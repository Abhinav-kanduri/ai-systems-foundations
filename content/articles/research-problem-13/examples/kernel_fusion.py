"""Demonstrate correctness; optionally time eager vs torch.compile.
This script makes NO promise that eager code or torch.compile always fuses.
"""
import time
import torch

device = 'cuda' if torch.cuda.is_available() else 'cpu'
x = torch.randn(1_000_000, device=device)

def baseline(x):
    a = x * 2.0
    b = a + 3.0
    return torch.relu(b)

def candidate(x):
    return torch.relu(x * 2.0 + 3.0)

def synchronize():
    if device == 'cuda':
        torch.cuda.synchronize()

def benchmark(fn, repeats=50, warmup=10):
    for _ in range(warmup):
        fn(x)
    synchronize()
    samples = []
    for _ in range(repeats):
        synchronize()
        before = time.perf_counter()
        fn(x)
        synchronize()
        samples.append((time.perf_counter() - before) * 1000)
    return sorted(samples)[len(samples) // 2]

expected = baseline(x)
torch.testing.assert_close(candidate(x), expected)
print('Correctness passed on', device)
print('Eager baseline median ms:', round(benchmark(baseline), 4))
print('Eager candidate median ms:', round(benchmark(candidate), 4))
if hasattr(torch, 'compile'):
    try:
        compiled = torch.compile(candidate)
        torch.testing.assert_close(compiled(x), expected)
        print('Compiled candidate median ms:', round(benchmark(compiled), 4))
    except Exception as exc:
        print('torch.compile unavailable for this environment:', type(exc).__name__, exc)
print('Review numerical tolerance, variability, and representative shapes before any claims.')
