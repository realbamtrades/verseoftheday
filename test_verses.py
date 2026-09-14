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

from verses import VERSES

TRANSLATION = os.getenv("TRANSLATION", "kjv")


async def check(session, reference, retries=3):
    url = f"https://bible-api.com/{quote(reference)}"
    for attempt in range(retries):
        try:
            async with session.get(url, params={"translation": TRANSLATION}, timeout=15) as resp:
                if resp.status == 429:
                    # Rate limited — back off and try again rather than failing it outright.
                    await asyncio.sleep(2 * (attempt + 1))
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


async def main():
    print(f"Checking {len(VERSES)} references against bible-api.com (translation={TRANSLATION})...")
    print("This goes one at a time with a short pause to avoid the free API's rate limit — it'll take a few minutes.\n")
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
            await asyncio.sleep(0.4)  # be polite to the free API

    print(f"\nDone. {len(VERSES) - len(failures)}/{len(VERSES)} references resolved successfully.")
    if failures:
        print("\nReferences to fix or remove from verses.py:")
        for reference, info in failures:
            print(f"  - {reference}  ({info})")
    else:
        print("All references are valid. ✅")


if __name__ == "__main__":
    asyncio.run(main())
