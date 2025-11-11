"""Build data structures for ranking heatmaps."""
from __future__ import annotations

from typing import Any, Dict, Iterable, List

import numpy as np


class HeatmapBuilder:
    def build(self, query: str, ranked_results: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
        scores = [max(min(item.get("score", 0.0), 1.0), 0.0) for item in ranked_results]
        if not scores:
            return {"values": [], "labels": [], "shape": (0, 0)}
        labels = [item.get("title", f"Result {idx + 1}") for idx, item in enumerate(ranked_results)]
        matrix = np.array(scores, dtype=float).reshape(1, -1)
        return {
            "values": matrix.tolist(),
            "labels": labels,
            "query": query,
            "shape": matrix.shape,
        }
