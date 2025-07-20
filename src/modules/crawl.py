import asyncio
import httpx
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from utils.logger import logger

async def fetch(client, url, timeout=10):
    try:
        resp = await client.get(url, timeout=timeout)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        logger.error(f"Error fetching {url}: {e}")
        return ''

async def parse_and_extract(text, base_url):
    soup = BeautifulSoup(text, 'html.parser')
    title = soup.title.string if soup.title else ''
    paragraphs = [p.get_text() for p in soup.find_all('p')]
    # Extract new links
    links = [urljoin(base_url, a['href']) for a in soup.find_all('a', href=True)]
    content = '\n'.join(paragraphs)
    return {'url': base_url, 'title': title, 'text': content, 'links': links}

async def crawl_pages(urls):
    async with httpx.AsyncClient(follow_redirects=True) as client:
        tasks = [fetch(client, url) for url in urls]
        pages_raw = await asyncio.gather(*tasks)
        tasks = [parse_and_extract(pages_raw[i], urls[i]) for i in range(len(urls))]
        pages = await asyncio.gather(*tasks)
    return pages
