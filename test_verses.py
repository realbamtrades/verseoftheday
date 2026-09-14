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


async def check(session, reference, retries=5):
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


async def main():
    print(f"Checking {len(VERSES)} references against bible-api.com (translation={TRANSLATION})...")
    print("This goes one at a time with pauses to respect the free API's rate limit — it can take 10-15 minutes for the full list. That's normal.\n")
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
