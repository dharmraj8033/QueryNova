"""Summarization helpers for QueryNova."""
from __future__ import annotations

import asyncio
from typing import Any, Dict, Iterable, List, Optional, Tuple

from modules.ai_filter import get_client as get_openai_client
from src.utils.logger import logger

_DEFAULT_MODEL = "gpt-4o-mini"


class Summarizer:
    """Leverages LLM to synthesize ranked results."""

    def __init__(self, model: str = _DEFAULT_MODEL) -> None:
        self.model = model

    async def summarize(
        self,
        query: str,
        ranked_results: List[Dict[str, Any]],
        knowledge_base: Optional[Any] = None,
    ) -> Tuple[Optional[str], List[str]]:
        if not ranked_results:
            return None, []

        loop = asyncio.get_event_loop()
        prompt = self._build_prompt(query, ranked_results, knowledge_base)
        try:
            client = get_openai_client()
        except Exception as exc:  # pragma: no cover - configuration runtime
            logger.warning("OpenAI client unavailable: %s", exc)
            return self._fallback_summary(ranked_results)

        def _invoke() -> Tuple[str, List[str]]:
            completion = client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are QueryNova's research analyst. Craft concise, decision-ready insight.",
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                max_tokens=400,
            )
            if not completion.choices:
                raise RuntimeError("Empty response from OpenAI")
            primary = completion.choices[0].message.content or ""
            bullets = self._extract_bullets(primary)
            intro = primary.split("\n\n", 1)[0]
            return intro.strip(), bullets

        try:
            summary, insights = await loop.run_in_executor(None, _invoke)
            return summary, insights
        except Exception as exc:  # pragma: no cover - depends on remote service
            logger.error("LLM summarization failed: %s", exc)
            return self._fallback_summary(ranked_results)

    def _build_prompt(
        self,
        query: str,
        ranked_results: List[Dict[str, Any]],
        knowledge_base: Optional[Any],
    ) -> str:
        def format_entry(idx: int, item: Dict[str, Any]) -> str:
            summary = item.get("summary", "")
            insight = item.get("insight", "")
            reliability = item.get("reliability", 0)
            return (
                f"Result {idx + 1}:\n"
                f"Title: {item.get('title', 'Untitled')}\n"
                f"URL: {item.get('url')}\n"
                f"Reliability: {reliability:.2f}\n"
                f"Summary: {summary}\n"
                f"Insight: {insight}\n"
            )

        buffer: List[str] = [f"Primary query: {query}", "\nRanked evidence:"]
        for idx, item in enumerate(ranked_results[:8]):
            buffer.append(format_entry(idx, item))

        if knowledge_base and knowledge_base.has_documents:
            buffer.append("\nCustom knowledge excerpts:")
            for doc in knowledge_base.get_top_snippets(query, limit=3):
                buffer.append(f"Source: {doc['name']}\nSnippet: {doc['snippet']}")

        buffer.append(
            "\nDeliver a 2-3 sentence executive summary followed by bullet insights with actionable findings."
        )
        return "\n".join(buffer)

    @staticmethod
    def _fallback_summary(ranked: List[Dict[str, Any]]) -> Tuple[str, List[str]]:
        snippets = [item.get("summary", "")[:200] for item in ranked[:3]]
        baseline = " ".join(snippets)
        summary = baseline[:500]
        insights = [f"#{idx + 1} {item.get('title', 'Untitled')}" for idx, item in enumerate(ranked[:5])]
        return summary, insights

    @staticmethod
    def _extract_bullets(text: str) -> List[str]:
        bullets: List[str] = []
        for line in text.splitlines():
            line = line.strip("-• ")
            if len(line.split()) > 3:
                bullets.append(line)
        return bullets[:8]
