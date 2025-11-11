"""Background jobs for QueryNova."""
from __future__ import annotations

import asyncio
from typing import Any, Dict

from src.services.search_service import SearchOptions, SearchPayload, SearchService
from src.tasks.celery_app import celery_app


@celery_app.task(bind=True, name="querynova.search")
def search_task(self, query: str, options: Dict[str, Any]) -> Dict[str, Any]:
    service = SearchService()
    payload = SearchPayload(query=query, options=SearchOptions(**options))
    result = asyncio.run(service.run(payload))
    return result


def enqueue_search(query: str, options: Dict[str, Any]):
    return search_task.delay(query, options)
