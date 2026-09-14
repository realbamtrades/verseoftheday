"""
Bam Trades / Trading Patiently Co. — Discord Verse of the Day Bot

Posts a random Bible verse every day at 9:00 AM Eastern Time (America/New_York,
handles EST/EDT automatically) into a specific channel, cycling through the
full list in verses.py without repeating a verse until every verse has been
used once.

Verse text is fetched live from bible-api.com so it's always accurate, and
you can change translations by editing TRANSLATION in your .env file.
"""

import asyncio
import json
import os
import random
from datetime import datetime
from pathlib import Path
from urllib.parse import quote
from zoneinfo import ZoneInfo

import aiohttp
import discord
from aiohttp import web
from discord.ext import tasks
from dotenv import load_dotenv

from verses import VERSES

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
TRANSLATION = os.getenv("TRANSLATION", "kjv")
POST_HOUR = int(os.getenv("POST_HOUR", "9"))  # 24-hour, in TIMEZONE below
PORT = int(os.getenv("PORT", "10000"))  # Render sets this automatically for Web Services
TIMEZONE = ZoneInfo("America/New_York")  # Eastern Time, auto-adjusts for DST

STATE_FILE = Path(__file__).parent / "state.json"

if not DISCORD_TOKEN:
    raise SystemExit("Missing DISCORD_TOKEN in your .env file.")
if not CHANNEL_ID:
    raise SystemExit("Missing CHANNEL_ID in your .env file.")
CHANNEL_ID = int(CHANNEL_ID)

intents = discord.Intents.default()
client = discord.Client(intents=intents)


# ---------- State handling (tracks which verses are left + last post date) ----------

def load_state() -> dict:
    if STATE_FILE.exists():
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {"queue": [], "last_posted": None}


def save_state(state: dict) -> None:
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def get_next_reference(state: dict) -> str:
    """Pop the next verse reference from the shuffled queue, reshuffling
    a fresh full cycle whenever the queue runs empty."""
    if not state["queue"]:
        fresh = VERSES.copy()
        random.shuffle(fresh)
        state["queue"] = fresh
    return state["queue"].pop(0)


# ---------- Fetching verse text ----------

async def fetch_verse(session: aiohttp.ClientSession, reference: str) -> dict | None:
    url = f"https://bible-api.com/{quote(reference)}"
    params = {"translation": TRANSLATION}
    for attempt in range(3):
        try:
            async with session.get(url, params=params, timeout=15) as resp:
                if resp.status == 429:
                    await asyncio.sleep(2 * (attempt + 1))
                    continue
                if resp.status != 200:
                    return None
                data = await resp.json()
                if "text" not in data:
                    return None
                return {
                    "reference": data.get("reference", reference),
                    "text": data["text"].strip().replace("\n", " "),
                    "translation": data.get("translation_name", TRANSLATION.upper()),
                }
        except Exception as e:
            print(f"[verse-bot] Error fetching '{reference}': {e}")
            return None
    return None


async def build_verse_embed(session: aiohttp.ClientSession, state: dict) -> discord.Embed | None:
    """Try up to 5 verses in case one reference fails to resolve."""
    for _ in range(5):
        reference = get_next_reference(state)
        verse = await fetch_verse(session, reference)
        if verse:
            embed = discord.Embed(
                title="📖 Verse of the Day",
                description=f'*"{verse["text"]}"*',
                color=discord.Color.gold(),
            )
            embed.set_footer(text=f'{verse["reference"]} ({verse["translation"]})')
            return embed
        print(f"[verse-bot] Skipping unresolved reference: {reference}")
    return None


# ---------- Daily posting loop ----------

@tasks.loop(seconds=60)
async def daily_verse_check():
    now = datetime.now(TIMEZONE)
    today_str = now.date().isoformat()
    state = load_state()

    if state.get("last_posted") == today_str:
        return  # already posted today
    if now.hour < POST_HOUR:
        return  # not time yet

    channel = client.get_channel(CHANNEL_ID)
    if channel is None:
        print(f"[verse-bot] Could not find channel with ID {CHANNEL_ID}. "
              f"Check CHANNEL_ID and that the bot has access to it.")
        return

    async with aiohttp.ClientSession() as session:
        embed = await build_verse_embed(session, state)

    if embed is None:
        print("[verse-bot] Failed to fetch a verse after several attempts; will retry next minute.")
        return

    await channel.send(embed=embed)
    state["last_posted"] = today_str
    save_state(state)
    print(f"[verse-bot] Posted verse of the day at {now.isoformat()}")


@daily_verse_check.before_loop
async def before_daily_verse_check():
    await client.wait_until_ready()


@client.event
async def on_ready():
    print(f"[verse-bot] Logged in as {client.user} (ID: {client.user.id})")
    print(f"[verse-bot] Watching for {POST_HOUR}:00 America/New_York daily, "
          f"posting to channel ID {CHANNEL_ID}")
    if not daily_verse_check.is_running():
        daily_verse_check.start()


# ---------- Tiny web server (required for Render's free Web Service tier) ----------
# Render's free plan only keeps "Web Services" (not Background Workers) at no cost,
# but a Web Service is expected to respond to HTTP requests. The bot itself doesn't
# need this for anything — it's purely so Render (and an external uptime pinger, see
# README) has something to check so the service doesn't get marked idle.

async def health_check(request):
    return web.Response(text="Verse bot is running.")


async def start_web_server():
    app = web.Application()
    app.router.add_get("/", health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    print(f"[verse-bot] Health-check web server listening on port {PORT}")


async def main():
    await start_web_server()
    await client.start(DISCORD_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
