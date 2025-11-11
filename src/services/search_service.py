"""High-level orchestration for QueryNova intelligent search."""
from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional

from tenacity import retry, stop_after_attempt, wait_exponential

from modules.search import search as serpapi_search
from modules.crawl import crawl_pages
from modules.ai_filter import rank_pages
from src.services.query_refinement import suggest_queries
from src.services.summarizer import Summarizer
from src.services.sentiment import SentimentAnalyzer
from src.services.heatmap import HeatmapBuilder
from src.services.export_service import ExportBuilder
from src.services.knowledge_base import KnowledgeBase
from src.utils import cache
from src.utils.logger import logger

ProgressHandler = Callable[[str, Dict[str, Any]], None]


@dataclass
class SearchOptions:
    limit: int = 10
    use_cache: bool = True
    include_sentiment: bool = True
    include_heatmap: bool = True
    include_summary: bool = True
    include_suggestions: bool = True
    include_knowledge: bool = True
    offline_mode: bool = False
    include_pdf: bool = False
    user_id: Optional[str] = None


@dataclass
class SearchPayload:
    query: str
    options: SearchOptions = field(default_factory=SearchOptions)
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class SearchService:
    """Coordinates the end-to-end search experience."""

    def __init__(self, knowledge_base: Optional[KnowledgeBase] = None) -> None:
        self.summarizer = Summarizer()
        self.sentiment = SentimentAnalyzer()
        self.heatmap = HeatmapBuilder()
        self.exporter = ExportBuilder()
        self.knowledge_base = knowledge_base or KnowledgeBase()

    async def run(self, payload: SearchPayload, progress: Optional[ProgressHandler] = None) -> Dict[str, Any]:
        def emit(stage: str, data: Optional[Dict[str, Any]] = None) -> None:
            if progress:
                progress(stage, data or {})

        query = payload.query.strip()
        if not query:
            raise ValueError("Query must not be empty")

        messages: List[Dict[str, str]] = []

        emit("start", {"query": query, "options": payload.options.__dict__})
        cache_key = f"{query}:{payload.options.limit}"
        if payload.options.use_cache:
            cached = cache.fetch_query(cache_key)
            if cached:
                cached.setdefault("messages", []).append({
                    "level": "info",
                    "text": "Loaded cached result snapshot.",
                })
                emit("cache_hit", {"count": len(cached.get("ranked", []))})
                exports, export_warnings = self.exporter.build_export_bundle(
                    query=cached.get("query", query),
                    ranked=cached.get("ranked") or [],
                    summary=cached.get("summary"),
                    insights=cached.get("insights") or [],
                    include_pdf=payload.options.include_pdf,
                )
                if export_warnings:
                    cached.setdefault("messages", []).extend(
                        [{"level": "warning", "text": warning} for warning in export_warnings]
                    )
                cached["exports"] = exports
                return cached

        results_raw: List[Dict[str, Any]] = []
        pages: List[Dict[str, Any]] = []
        if not payload.options.offline_mode:
            emit("searching", {"provider": "SerpAPI"})
            try:
                results_raw = await self._search_with_retry(query, payload.options.limit)
                emit("search_complete", {"count": len(results_raw)})
            except ValueError as exc:
                detail = str(exc) or "SerpAPI search failed."
                messages.append({"level": "error", "text": detail})
                emit("search_failed", {"reason": detail})
            except Exception as exc:
                import traceback
                error_trace = traceback.format_exc()
                logger.error("Search provider error: %s\n%s", exc, error_trace)
                
                # Provide specific error messages
                error_msg = str(exc)
                if "401" in error_msg or "Unauthorized" in error_msg:
                    detail = "❌ API Key Error: SerpAPI key is invalid or expired. Check .streamlit/secrets.toml"
                elif "429" in error_msg or "rate limit" in error_msg.lower():
                    detail = "⚠️ Rate Limit: Too many requests. Try again in a few minutes."
                elif "timeout" in error_msg.lower():
                    detail = "⏱️ Timeout: Search request took too long. Try again."
                else:
                    detail = f"❌ Search Error: {error_msg}"
                
                messages.append({"level": "error", "text": detail})
                emit("search_failed", {"reason": detail})
        else:
            emit("offline_mode", {})

        if not results_raw and payload.options.offline_mode:
            cached_snapshot = cache.fetch_query(cache_key)
            if cached_snapshot:
                emit("offline_cache", {"count": len(cached_snapshot.get("ranked", []))})
                cached_snapshot.setdefault("messages", []).append({
                    "level": "info",
                    "text": "Served from offline cache.",
                })
                exports, export_warnings = self.exporter.build_export_bundle(
                        query=cached_snapshot.get("query", query),
                        ranked=cached_snapshot.get("ranked") or [],
                        summary=cached_snapshot.get("summary"),
                        insights=cached_snapshot.get("insights") or [],
                        include_pdf=payload.options.include_pdf,
                    )
                if export_warnings:
                    cached_snapshot.setdefault("messages", []).extend(
                        [{"level": "warning", "text": warning} for warning in export_warnings]
                    )
                cached_snapshot["exports"] = exports
                return cached_snapshot
            raise RuntimeError("No cached data available for offline mode")

        if results_raw:
            urls = [r["link"] for r in results_raw]
            emit("crawling", {"count": len(urls)})
            pages = await crawl_pages(urls, progress_handler=lambda meta: emit("crawl_progress", meta))
            emit("crawl_complete", {"count": len(pages)})

        emit("ranking", {})
        ranked = rank_pages(query, pages, knowledge_base=self.knowledge_base)
        emit("ranking_complete", {"count": len(ranked)})

        summary = None
        insights: List[str] = []
        if ranked and payload.options.include_summary:
            summary, insights = await self.summarizer.summarize(query, ranked, self.knowledge_base)
            emit("summary_ready", {"insight_count": len(insights)})

        suggestions: List[str] = []
        if payload.options.include_suggestions:
            suggestions = suggest_queries(query, ranked)
            emit("suggestions_ready", {"count": len(suggestions)})

        sentiments: Dict[str, Any] = {}
        if payload.options.include_sentiment and ranked:
            sentiments = self.sentiment.evaluate(ranked)
            emit("sentiment_ready", {"labels": list(sentiments.keys())})

        heatmap = None
        if payload.options.include_heatmap and ranked:
            heatmap = self.heatmap.build(query, ranked)
            emit("heatmap_ready", {"shape": heatmap.get("shape")})

        knowledge_context = None
        if payload.options.include_knowledge and self.knowledge_base.has_documents:
            knowledge_context = self.knowledge_base.to_dict()
            emit("knowledge_ready", {"documents": len(knowledge_context.get("documents", []))})

        if not ranked and not messages:
            messages.append({
                "level": "info",
                "text": "No live results were retrieved. Add API keys or upload knowledge assets to enrich responses.",
            })

        export_bundle, export_warnings = self.exporter.build_export_bundle(
            query=query,
            ranked=ranked,
            summary=summary,
            insights=insights,
                include_pdf=payload.options.include_pdf,
            )
        emit("exports_ready", {"formats": list(export_bundle.keys())})
        for warning in export_warnings:
            messages.append({"level": "warning", "text": warning})

        response = {
            "query": query,
            "ranked": ranked,
            "raw_results": results_raw,
            "summary": summary,
            "insights": insights,
            "suggestions": suggestions,
            "sentiment": sentiments,
            "heatmap": heatmap,
            "knowledge": knowledge_context,
            "exports": export_bundle,
            "metadata": {
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "options": payload.options.__dict__,
            },
            "messages": messages,
        }

        cache_payload = dict(response)
        cache_payload["exports"] = None
        cache.store_query(cache_key, cache_payload)
        emit("complete", {"cached": True})
        return response

    @staticmethod
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=8), reraise=True)
    async def _search_with_retry(query: str, limit: int) -> List[Dict[str, Any]]:
        loop = asyncio.get_running_loop()
        # Run blocking SerpAPI call in thread executor
        return await loop.run_in_executor(None, lambda: serpapi_search(query, num=limit))


async def execute_search(query: str, options: Optional[Dict[str, Any]] = None, progress: Optional[ProgressHandler] = None) -> Dict[str, Any]:
    service = SearchService()
    payload = SearchPayload(query=query, options=SearchOptions(**(options or {})))
    return await service.run(payload, progress=progress)
