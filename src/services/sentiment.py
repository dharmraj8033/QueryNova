"""Sentiment analysis helpers for search results."""
from __future__ import annotations

from typing import Any, Dict, Iterable

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class SentimentAnalyzer:
    """Wraps Vader sentiment scoring."""

    def __init__(self) -> None:
        self._analyzer = SentimentIntensityAnalyzer()

    def evaluate(self, ranked_results: Iterable[Dict[str, Any]]) -> Dict[str, float]:
        aggregate = {"positive": 0.0, "neutral": 0.0, "negative": 0.0}
        total = 0
        for item in ranked_results:
            summary = item.get("summary") or ""
            scores = self._analyzer.polarity_scores(summary)
            aggregate["positive"] += scores.get("pos", 0.0)
            aggregate["neutral"] += scores.get("neu", 0.0)
            aggregate["negative"] += scores.get("neg", 0.0)
            total += 1
        if not total:
            return aggregate
        return {key: value / total for key, value in aggregate.items()}
