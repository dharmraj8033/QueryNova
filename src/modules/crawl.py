import asyncio
from functools import lru_cache
from typing import Any, Callable, Dict, Iterable, List, Optional

import httpx
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_exponential
from urllib.parse import urljoin

from src.plugins.registry import registry
from src.utils.logger import logger

Progress = Callable[[Dict[str, Any]], None]

_CACHE: Dict[str, Dict[str, Any]] = {}


async def crawl_pages(urls: Iterable[str], progress_handler: Optional[Progress] = None) -> List[Dict[str, Any]]:
    semaphore = asyncio.Semaphore(8)
    async with httpx.AsyncClient(follow_redirects=True, timeout=15) as client:
        tasks = [
            _crawl_single(url, client, semaphore, progress_handler)
            for url in urls
        ]
        return await asyncio.gather(*tasks)


async def _crawl_single(
    url: str,
    client: httpx.AsyncClient,
    semaphore: asyncio.Semaphore,
    progress_handler: Optional[Progress],
) -> Dict[str, Any]:
    if url in _CACHE:
        return _CACHE[url]

    await semaphore.acquire()
    try:
        if progress_handler:
            progress_handler({"url": url, "status": "fetching"})
        try:
            text = await _fetch_with_retry(client, url)
        except Exception as exc:
            logger.error("Fetch failed for %s: %s", url, exc)
            return {"url": url, "title": url, "text": "", "links": []}
        if progress_handler:
            progress_handler({"url": url, "status": "parsing"})
        try:
            page = await _parse_and_extract(text, url)
        except Exception as exc:
            logger.error("Parse failed for %s: %s", url, exc)
            page = {"url": url, "title": url, "text": text[:5000], "links": []}
        for name, crawler in registry.crawlers.items():
            try:
                extra = crawler(url)
                page.setdefault("metadata", {}).setdefault("plugins", {})[name] = extra
            except Exception as exc:
                logger.error("Plugin crawler failed (%s): %s", name, exc)
        _CACHE[url] = page
        if progress_handler:
            progress_handler({"url": url, "status": "complete"})
        return page
    finally:
        semaphore.release()


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
async def _fetch_with_retry(client: httpx.AsyncClient, url: str) -> str:
    response = await client.get(url)
    response.raise_for_status()
    return response.text


async def _parse_and_extract(text: str, base_url: str) -> Dict[str, Any]:
    soup = BeautifulSoup(text, "html.parser")
    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
    links = [urljoin(base_url, a["href"]) for a in soup.find_all("a", href=True)]
    content = "\n".join(paragraphs)
    return {
        "url": base_url,
        "title": title or base_url,
        "text": content,
        "links": links,
    }
