"""
Run this once before you deploy (and again any time you edit verses.py) to
confirm every reference in the list actually resolves via bible-api.com.

    python test_verses.py

It will print any references that failed to resolve so you can fix or
remove them.
"""

import asyncio
import os
from urllib.parse import quote

import aiohttp
from bs4 import BeautifulSoup

from verses import VERSES

TRANSLATION = os.getenv("TRANSLATION", "kjv")
NLT_API_KEY = os.getenv("NLT_API_KEY", "TEST")


def _parse_nlt_html(html: str) -> str | None:
    soup = BeautifulSoup(html, "html.parser")
    container = soup.find(id="bibletext")
    if container is None:
        return None
    for tag in container.find_all(class_=["a-tn", "tn", "vn", "bk_ch_vs_header", "subhead", "chapter-number"]):
        tag.decompose()
    text = " ".join(container.get_text(separator=" ", strip=True).split())
    return text or None


async def check_nlt(session, reference, retries=3):
    url = "https://api.nlt.to/api/passages"
    for attempt in range(retries):
        try:
            async with session.get(url, params={"ref": reference, "key": NLT_API_KEY}, timeout=15) as resp:
                if resp.status == 429:
                    await asyncio.sleep(3 * (2 ** attempt))
                    continue
                if resp.status != 200:
                    return reference, False, f"HTTP {resp.status}"
                text = _parse_nlt_html(await resp.text())
                if not text:
                    return reference, False, "empty/unparseable response"
                return reference, True, text[:60]
        except Exception as e:
            return reference, False, str(e)
    return reference, False, "rate limited after retries"


async def check_bible_api(session, reference, retries=5):
    url = f"https://bible-api.com/{quote(reference)}"
    for attempt in range(retries):
        try:
            async with session.get(url, params={"translation": TRANSLATION}, timeout=15) as resp:
                if resp.status == 429:
                    # Rate limited — back off harder each time rather than failing it outright.
                    await asyncio.sleep(3 * (2 ** attempt))
                    continue
                if resp.status != 200:
                    return reference, False, f"HTTP {resp.status}"
                data = await resp.json()
                if "text" not in data or not data["text"].strip():
                    return reference, False, "empty text in response"
                return reference, True, data["text"].strip()[:60]
        except Exception as e:
            return reference, False, str(e)
    return reference, False, "HTTP 429 (rate limited after retries)"


async def check(session, reference):
    if TRANSLATION.lower() == "nlt":
        return await check_nlt(session, reference)
    return await check_bible_api(session, reference)


async def main():
    source = "api.nlt.to" if TRANSLATION.lower() == "nlt" else "bible-api.com"
    print(f"Checking {len(VERSES)} references against {source} (translation={TRANSLATION})...")
    print("This goes one at a time with pauses to respect rate limits — it can take 10-15 minutes for the full list. That's normal.\n")
    failures = []
    async with aiohttp.ClientSession() as session:
        for i, reference in enumerate(VERSES, start=1):
            result = await check(session, reference)
            _, ok, info = result
            if not ok:
                failures.append((reference, info))
                print(f"  ❌ {reference}  ->  {info}")
            elif i % 25 == 0:
                print(f"  ...{i}/{len(VERSES)} checked")
            await asyncio.sleep(1.2)  # be polite to the free API

    print(f"\nDone with first pass. {len(VERSES) - len(failures)}/{len(VERSES)} resolved.")

    if failures:
        print(f"\nRetrying {len(failures)} that failed (rate limit window has likely reset by now)...\n")
        still_failing = []
        async with aiohttp.ClientSession() as session:
            for reference, _ in failures:
                result = await check(session, reference)
                _, ok, info = result
                if not ok:
                    still_failing.append((reference, info))
                    print(f"  ❌ {reference}  ->  {info}")
                await asyncio.sleep(1.2)
        failures = still_failing

    print(f"\nFinal result: {len(VERSES) - len(failures)}/{len(VERSES)} references resolved successfully.")
    if failures:
        print("\nReferences to fix or remove from verses.py:")
        for reference, info in failures:
            print(f"  - {reference}  ({info})")
    else:
        print("All references are valid. ✅")


if __name__ == "__main__":
    asyncio.run(main())
