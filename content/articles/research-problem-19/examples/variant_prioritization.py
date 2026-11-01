"""Synthetic educational variant prioritization; NOT AlphaGenome/AVI scoring."""
import pandas as pd

variants = pd.DataFrame({
    "variant": ["V1", "V2", "V3", "V4"],
    "predicted_impact": [0.91, 0.78, 0.65, 0.88],
    "tissue_relevance": [0.40, 0.95, 0.85, 0.60],
    "uncertainty": [0.35, 0.10, 0.20, 0.45],
})

# Fictional ranking weights; not a published AlphaGenome formula.
variants["priority_score"] = (
    0.50 * variants["predicted_impact"]
    + 0.35 * variants["tissue_relevance"]
    - 0.15 * variants["uncertainty"]
)
print(variants.sort_values("priority_score", ascending=False).to_string(index=False))
