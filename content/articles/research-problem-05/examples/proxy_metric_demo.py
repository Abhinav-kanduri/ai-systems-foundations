"""Hypothetical illustration: proxy rewards vs verified outcomes. No external packages."""
records = [
    {"ticket": "A", "closed": True, "verified_resolved": True},
    {"ticket": "B", "closed": True, "verified_resolved": False},
    {"ticket": "C", "closed": True, "verified_resolved": False},
    {"ticket": "D", "closed": True, "verified_resolved": True},
    {"ticket": "E", "closed": False, "verified_resolved": False},
]
closed = sum(r["closed"] for r in records)
resolved = sum(r["verified_resolved"] for r in records)
print(f"Closed (proxy): {closed}/{len(records)}")
print(f"Independently verified resolved (outcome): {resolved}/{len(records)}")
assert resolved <= closed
