import html2text
import asyncio
import aiohttp
import re


async def fetch_url(session, url):
    async with session.get(url) as response:
        try:
            response.raise_for_status()
            response.encoding = 'utf-8'
            html = await response.text()

            return html
        except Exception as e:
            print(f"fetch url failed: {url}: {e}")
            return ""


async def html_to_markdown(html):
    try:
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True

        markdown = h.handle(html)

        return markdown
    except Exception as e:
        print(f"html to markdown failed: {e}")
        return ""


async def fetch_markdown(session, url):
    try:
        html = await fetch_url(session, url)
        markdown = await html_to_markdown(html)
        markdown = re.sub(r'\n{2,n}', '\n', markdown)

        return url, markdown
    except Exception as e:
        print(f"fetch markdown failed: {url}: {e}")
        return url, ""


async def batch_fetch_urls(urls):
    print("urls", urls)
    try:
        async with aiohttp.ClientSession() as session:
            tasks = [fetch_markdown(session, url) for url in urls]
            results = await asyncio.gather(*tasks, return_exceptions=False)

            return results
    except aiohttp.ClientResponseError as e:
        print(f"batch fetch urls failed: {e}")
        return []
