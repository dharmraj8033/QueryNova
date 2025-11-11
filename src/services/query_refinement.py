"""Generate related queries using lightweight heuristics and embeddings when available."""
from __future__ import annotations

import itertools
import re
from collections import Counter
from typing import Dict, Iterable, List

try:  # pragma: no cover - optional dependency on OpenAI embeddings
    from modules.ai_filter import get_embedding
except Exception:  # pragma: no cover
    get_embedding = None  # type: ignore

_STOPWORDS = {
    "the",
    "and",
    "or",
    "to",
    "of",
    "a",
    "is",
    "on",
    "for",
    "in",
    "how",
    "what",
    "why",
    "when",
    "vs",
}


def suggest_queries(query: str, ranked_results: Iterable[Dict[str, str]], limit: int = 6) -> List[str]:
    terms = _extract_terms(query)
    corpus = " ".join(item.get("summary", "") for item in ranked_results)
    keywords = _extract_terms(corpus)
    counts = Counter(keywords)
    candidates = [k for k, _ in counts.most_common(12) if k not in terms]

    suggestions: List[str] = []
    for combo in itertools.combinations(sorted(set(terms + candidates)), 2):
        suggestion = " ".join(combo)
        if suggestion.lower() != query.lower():
            suggestions.append(f"{suggestion} insights")
        if len(suggestions) >= limit:
            break

    if get_embedding:
        suggestions = _rerank_by_embedding(query, suggestions)
    return suggestions[:limit]


def _extract_terms(text: str) -> List[str]:
    tokens = re.findall(r"[A-Za-z0-9]+", text.lower())
    return [token for token in tokens if token not in _STOPWORDS and len(token) > 2]


def _rerank_by_embedding(query: str, suggestions: List[str]) -> List[str]:  # pragma: no cover - remote call
    try:
        query_vec = get_embedding(query)
        scored = []
        for suggestion in suggestions:
            vec = get_embedding(suggestion)
            score = sum(a * b for a, b in zip(query_vec, vec))
            scored.append((score, suggestion))
        scored.sort(reverse=True)
        return [s for _, s in scored]
    except Exception:
        return suggestions
