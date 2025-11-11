"""Local caching utilities leveraging SQLite for offline resilience."""
from __future__ import annotations

import json
import os
import sqlite3
import threading
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, Optional

_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "query_cache.db")
_LOCK = threading.Lock()


def _ensure_db() -> None:
    os.makedirs(os.path.dirname(_DB_PATH), exist_ok=True)
    with sqlite3.connect(_DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL,
                results TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_queries_query
            ON queries(query)
            """
        )
        conn.commit()


@contextmanager
def _connect() -> Iterable[sqlite3.Connection]:
    _ensure_db()
    with _LOCK:
        conn = sqlite3.connect(_DB_PATH)
        try:
            yield conn
        finally:
            conn.close()


def store_query(query: str, results: Dict[str, Any]) -> None:
    payload = json.dumps(results)
    with _connect() as conn:
        conn.execute(
            "INSERT INTO queries (query, results, created_at) VALUES (?, ?, ?)",
            (query, payload, datetime.now(timezone.utc).isoformat()),
        )
        conn.commit()


def fetch_query(query: str) -> Optional[Dict[str, Any]]:
    with _connect() as conn:
        row = conn.execute(
            "SELECT results FROM queries WHERE query = ? ORDER BY created_at DESC LIMIT 1",
            (query,),
        ).fetchone()
    if not row:
        return None
    return json.loads(row[0])


def recent_queries(limit: int = 20) -> Iterable[Dict[str, Any]]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT query, results, created_at FROM queries ORDER BY created_at DESC LIMIT ?",
            (limit,),
        ).fetchall()
    for query, payload, created_at in rows:
        yield {
            "query": query,
            "results": json.loads(payload),
            "created_at": created_at,
        }
