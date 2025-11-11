"""Flask API exposing QueryNova services."""
from __future__ import annotations

import asyncio
import json
from datetime import datetime, timezone
from typing import Any, Dict

from celery.result import AsyncResult
from flask import Flask, jsonify, request
from flask_socketio import SocketIO

from src.services.search_service import SearchOptions, SearchPayload, SearchService
from src.tasks.jobs import enqueue_search
from src.utils.logger import logger

app = Flask(__name__)
app.config["SECRET_KEY"] = "querynova-secret"
socketio = SocketIO(app, cors_allowed_origins="*")
service = SearchService()


@app.route("/api/health")
def health() -> Any:
    return jsonify({"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()})


@app.route("/api/search", methods=["POST"])
def trigger_search() -> Any:
    payload = request.get_json(force=True) or {}
    query = payload.get("query", "").strip()
    if not query:
        return jsonify({"error": "Query is required"}), 400

    use_background = payload.get("background", False)
    options = SearchOptions(**payload.get("options", {}))

    if use_background:
        job = enqueue_search(query, options.__dict__)
        return jsonify({"job_id": job.id})

    def _progress(stage: str, meta: Dict[str, Any]) -> None:
        socketio.emit("search_progress", {"stage": stage, "meta": meta})

    result = asyncio.run(service.run(SearchPayload(query=query, options=options), progress=_progress))
    return jsonify(result)


@app.route("/api/jobs/<job_id>")
def job_status(job_id: str) -> Any:
    async_result = AsyncResult(job_id)
    if async_result.state == "PENDING":
        return jsonify({"status": "pending"})
    if async_result.state == "FAILURE":
        return jsonify({"status": "failed", "error": str(async_result.info)}), 500
    return jsonify({"status": async_result.state.lower(), "result": async_result.result})


@app.route("/metrics")
def metrics() -> Any:
    payload = {
    "search_requests_total": socketio.server.manager.get_participants("/", "search_progress") if socketio.server else 0,
    "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    return app.response_class(json.dumps(payload), mimetype="application/json")


@socketio.on("connect")
def on_connect() -> None:
    logger.info("Client connected to WebSocket")


@socketio.on("disconnect")
def on_disconnect() -> None:
    logger.info("Client disconnected from WebSocket")


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8001)
