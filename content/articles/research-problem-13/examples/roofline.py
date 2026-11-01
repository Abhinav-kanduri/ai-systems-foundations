"""Illustrative Roofline example; runs on CPU."""
import numpy as np
import matplotlib.pyplot as plt
peak_tflops, bandwidth_tbps = 100., 2.
intensity = np.logspace(-1, 3, 500)
ceiling = np.minimum(peak_tflops, bandwidth_tbps * intensity)
print('Ridge (FLOPs/byte):', peak_tflops / bandwidth_tbps)
print('Ceiling at I=10 (TFLOP/s):', min(peak_tflops, bandwidth_tbps * 10))
plt.plot(intensity, ceiling)
plt.xscale('log')
plt.xlabel('Arithmetic intensity (FLOPs / byte)')
plt.ylabel('Upper bound (TFLOP/s)')
plt.title('Illustrative Roofline ceiling, not measured GPU performance')
plt.grid(True)
plt.tight_layout()
plt.show()
