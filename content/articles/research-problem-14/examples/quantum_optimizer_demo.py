"""CPU-only circuit identity and Qiskit transpiler demonstration."""
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Operator

original = QuantumCircuit(1)
original.h(0)
original.h(0)
identity = QuantumCircuit(1)

assert Operator(original).equiv(Operator(identity))
compiled = transpile(original, optimization_level=3)
assert Operator(original).equiv(Operator(compiled))

print("Original gates:", original.size())
print("Compiled gates:", compiled.size())
print("Original depth:", original.depth())
print("Compiled depth:", compiled.depth())
print("Equivalent (up to global phase):", Operator(original).equiv(Operator(compiled)))
