"""Simple local knowledge base to augment search results."""
from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from typing import Dict, Iterable, List

import requests
from pypdf import PdfReader

from src.utils.logger import logger

_KNOWLEDGE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "data", "knowledge")


@dataclass
class KnowledgeDocument:
    name: str
    content: str


@dataclass
class KnowledgeBase:
    documents: List[KnowledgeDocument] = field(default_factory=list)

    def __post_init__(self) -> None:
        os.makedirs(_KNOWLEDGE_DIR, exist_ok=True)

    @property
    def has_documents(self) -> bool:
        return len(self.documents) > 0

    def ingest_file(self, filename: str, file_bytes: bytes) -> None:
        path = os.path.join(_KNOWLEDGE_DIR, filename)
        with open(path, "wb") as handle:
            handle.write(file_bytes)
        content = self._extract_content(path)
        self.documents.append(KnowledgeDocument(name=filename, content=content))
        logger.info("Ingested custom knowledge file: %s", filename)

    def ingest_url(self, url: str) -> None:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        text = response.text
        name = re.sub(r"[^A-Za-z0-9]+", "_", url)[:60]
        self.documents.append(KnowledgeDocument(name=name, content=text))
        logger.info("Ingested custom knowledge url: %s", url)

    def get_top_snippets(self, query: str, limit: int = 3) -> List[Dict[str, str]]:
        snippets: List[Dict[str, str]] = []
        for doc in self.documents:
            matches = self._find_matches(query, doc.content)
            for match in matches[:limit]:
                snippets.append({"name": doc.name, "snippet": match})
        return snippets[:limit]

    def to_dict(self) -> Dict[str, Iterable[str]]:
        return {
            "documents": [doc.name for doc in self.documents],
            "total": len(self.documents),
        }

    def _extract_content(self, path: str) -> str:
        if path.lower().endswith(".pdf"):
            reader = PdfReader(path)
            texts = [page.extract_text() or "" for page in reader.pages]
            return "\n".join(texts)
        with open(path, "r", encoding="utf-8", errors="ignore") as handle:
            return handle.read()

    def _find_matches(self, query: str, content: str) -> List[str]:
        pattern = re.compile(rf"(.{{0,120}}{re.escape(query)}.{{0,120}})", re.IGNORECASE)
        return [match.strip() for match in pattern.findall(content)]