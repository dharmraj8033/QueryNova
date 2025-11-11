"""Plugin registry allowing extensions for crawlers and renderers."""
from __future__ import annotations

from typing import Callable, Dict, List

from src.utils.logger import logger

CrawlerHook = Callable[[str], Dict[str, str]]
RendererHook = Callable[[Dict[str, str]], Dict[str, str]]


class PluginRegistry:
    def __init__(self) -> None:
        self._crawlers: Dict[str, CrawlerHook] = {}
        self._renderers: Dict[str, RendererHook] = {}

    def register_crawler(self, name: str, handler: CrawlerHook) -> None:
        self._crawlers[name] = handler
        logger.info("Registered crawler plugin: %s", name)

    def register_renderer(self, name: str, handler: RendererHook) -> None:
        self._renderers[name] = handler
        logger.info("Registered renderer plugin: %s", name)

    @property
    def crawlers(self) -> Dict[str, CrawlerHook]:
        return dict(self._crawlers)

    @property
    def renderers(self) -> Dict[str, RendererHook]:
        return dict(self._renderers)

    def list_plugins(self) -> Dict[str, List[str]]:
        return {
            "crawlers": list(self._crawlers.keys()),
            "renderers": list(self._renderers.keys()),
        }


registry = PluginRegistry()