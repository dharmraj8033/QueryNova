import re
from typing import Any, Dict, Iterable, Optional

import numpy as np
from urllib.parse import urlparse

from src.utils.logger import logger
from src.utils.ai_provider import get_ai_provider


def get_embedding(text: str) -> Iterable[float]:
    """Get text embedding using the configured AI provider (Gemini or OpenAI)."""
    provider = get_ai_provider()
    embedding = provider.get_embedding(text)
    if embedding:
        return embedding
    # Fallback to empty embedding
    logger.warning("No embedding available, using fallback")
    return [0.0] * 384  # Default embedding size


def cosine_similarity(a: Iterable[float], b: Iterable[float]) -> float:
    vec_a = np.array(list(a))
    vec_b = np.array(list(b))
    denom = np.linalg.norm(vec_a) * np.linalg.norm(vec_b)
    if not denom:
        return 0.0
    return float(np.dot(vec_a, vec_b) / denom)


def rank_pages(query: str, pages: Iterable[Dict[str, Any]], knowledge_base: Optional[Any] = None) -> Iterable[Dict[str, Any]]:
    pages = list(pages)
    if not pages:
        return []

    try:
        query_emb = list(get_embedding(query))
    except Exception as exc:
        logger.warning("Embedding failed for query: %s", exc)
        query_emb = []

    ranked = []
    for page in pages:
        text = (page.get("text") or "")[:4000]
        try:
            emb = list(get_embedding(text)) if query_emb else []
            score = cosine_similarity(query_emb, emb) if query_emb and emb else lexical_overlap(query, text)
        except Exception as exc:
            logger.warning("Embedding failed for page %s: %s", page.get("url"), exc)
            score = lexical_overlap(query, text)

        reliability = domain_reliability(page.get("url", ""))
        combined = min(max((score * 0.7) + (reliability * 0.3), 0.0), 1.0)
        summary, insight = summarize_passage(text)

        if knowledge_base and knowledge_base.has_documents:
            top_snippets = knowledge_base.get_top_snippets(query, limit=1)
        else:
            top_snippets = []

        ranked.append(
            {
                "url": page.get("url"),
                "title": page.get("title") or page.get("url"),
                "summary": summary,
                "insight": insight,
                "score": combined,
                "reliability": reliability,
                "snippets": top_snippets,
            }
        )

    ranked.sort(key=lambda item: item.get("score", 0), reverse=True)
    return ranked


def lexical_overlap(query: str, text: str) -> float:
    query_terms = set(re.findall(r"[A-Za-z0-9]+", query.lower()))
    text_terms = set(re.findall(r"[A-Za-z0-9]+", text.lower()))
    if not query_terms or not text_terms:
        return 0.0
    intersect = query_terms.intersection(text_terms)
    return float(len(intersect) / len(query_terms))


def domain_reliability(url: str) -> float:
    if not url:
        return 0.2
    domain = urlparse(url).netloc.lower()
    tiers = {
        "edu": 0.95,
        "gov": 0.9,
        "org": 0.8,
        "news": 0.75,
        "blog": 0.55,
    }
    for key, value in tiers.items():
        if domain.endswith(key):
            return value
    return 0.6


def summarize_passage(text: str) -> tuple[str, str]:
    """Summarize a text passage using the configured AI provider."""
    shortened = text[:1500]
    if not shortened.strip():
        return "No content available.", ""
    
    provider = get_ai_provider()
    if not provider.is_available():
        return _fallback_summary(shortened)

    try:
        summary_text = provider.generate_text(
            prompt=shortened,
            system_prompt="Produce a two sentence summary and one actionable insight.",
            max_tokens=180
        )
        
        if not summary_text:
            return _fallback_summary(shortened)
        
        summary_lines = [line.strip() for line in summary_text.split("\n") if line.strip()]
        summary = summary_lines[0] if summary_lines else summary_text[:280]
        insight = summary_lines[1] if len(summary_lines) > 1 else ""
        return summary, insight
    except Exception as exc:
        logger.warning("LLM summary fallback: %s", exc)
        return _fallback_summary(shortened)


def _fallback_summary(text: str) -> tuple[str, str]:
    sentences = re.split(r"(?<=[.!?]) +", text)
    summary = " ".join(sentences[:2])
    insight = sentences[2][:160] if len(sentences) > 2 else ""
    return summary or text[:200], insight
