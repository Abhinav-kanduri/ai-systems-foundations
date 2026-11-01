"""CPU-only illustration of evolutionary numeric search, NOT AlphaEvolve itself."""
import random

random.seed(42)

def objective(x: float) -> float:
    return (x - 7) ** 2 + 3

population = [random.uniform(-20, 20) for _ in range(20)]
for generation in range(30):
    population.sort(key=objective)
    elite = population[:5]
    offspring = []
    for _ in range(15):
        parent = random.choice(elite)
        child = parent + random.gauss(0, 2)
        offspring.append(child)
    population = elite + offspring

best = min(population, key=objective)
print("Best solution:", round(best, 4))
print("Objective value:", round(objective(best), 4))
print("Known optimum: x = 7, f(x) = 3")
