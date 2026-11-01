"""CPU-only teaching simulator: proposed actions must pass shared constraints."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Metrics:
    current_gpus: int = 100
    workload_units: int = 360
    gpu_cost_per_hour: float = 2.0
    p99_target_ms: float = 350.0
    min_spare_gpus: int = 10
    gpu_budget_hourly: float = 190.0
    state_revision: int = 42

def estimated_p99_ms(workload_units: int, gpus: int) -> float:
    """Toy curve, NOT a production latency model."""
    return 100.0 + 45.0 * workload_units / gpus

def cost_agent(m: Metrics) -> int:
    return max(1, int(m.current_gpus * 0.7))

def performance_agent(m: Metrics) -> int:
    return int(m.current_gpus * 1.15)

def reliability_agent(m: Metrics) -> int:
    return m.current_gpus  # retain capacity until feasibility proven

def feasible(m: Metrics, gpus: int) -> bool:
    needed = (m.workload_units + 4) // 5  # toy base working capacity
    return (gpus >= needed + m.min_spare_gpus
            and estimated_p99_ms(m.workload_units, gpus) <= m.p99_target_ms
            and gpus * m.gpu_cost_per_hour <= m.gpu_budget_hourly)

def deterministic_baseline(m: Metrics) -> int | None:
    for gpus in range(1, 1001):
        if feasible(m, gpus):
            return gpus
    return None

def coordinator(m: Metrics, proposals: dict[str,int], expected_revision: int) -> dict:
    if expected_revision != m.state_revision:
        return {'approved': False, 'reason': 'stale evidence revision', 'candidate': None}
    # proposals are advisory; evaluate both them and a deterministic safe baseline
    options = sorted(set(proposals.values()) | ({deterministic_baseline(m)} - {None}))
    safe = [g for g in options if feasible(m, g)]
    if not safe:
        return {'approved': False, 'reason': 'no feasible candidate', 'candidate': None}
    candidate = min(safe)
    return {'approved': True, 'reason': 'passes toy constraints; human approval still required', 'candidate': candidate}

def main():
    m = Metrics()
    proposals = {'cost': cost_agent(m), 'performance': performance_agent(m), 'reliability': reliability_agent(m)}
    print('Snapshot revision:', m.state_revision)
    print('Agent proposals:', proposals)
    print('Deterministic baseline:', deterministic_baseline(m))
    print('Coordinator:', coordinator(m, proposals, expected_revision=m.state_revision))

if __name__ == '__main__':
    main()
