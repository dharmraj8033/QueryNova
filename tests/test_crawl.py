import pytest
import asyncio
from src.modules.crawl import crawl_pages

@pytest.mark.asyncio
async def test_crawl_empty():
    pages = await crawl_pages([])
    assert pages == []

@pytest.mark.asyncio
async def test_crawl_invalid_url():
    pages = await crawl_pages(["http://invalid.url"])
    assert isinstance(pages, list)
