# Verse of the Day — Discord Bot

Posts a random Bible verse every day at **9:00 AM Eastern Time** into one
channel of your Discord server. Cycles through 329 popular/meaningful verses
(see `verses.py`) without repeating any until the whole list has been used,
then reshuffles and starts a new cycle. Verse text is pulled live from the
free [bible-api.com](https://bible-api.com) API (KJV by default), so it's
always accurate and you can switch translations with one setting.

---

## 1. Create the Discord bot

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications) → **New Application**. Name it whatever you want.
2. Left sidebar → **Bot** → **Add Bot**.
3. Under **Token**, click **Reset Token** and copy it. This is your `DISCORD_TOKEN`. Keep it secret — anyone with it can control the bot.
4. No privileged intents are needed (the bot only sends messages, it doesn't read them).
5. Left sidebar → **OAuth2 → URL Generator**:
   - Scopes: check `bot`
   - Bot Permissions: check `Send Messages` and `Embed Links`
   - Copy the generated URL at the bottom, open it in your browser, and invite the bot to your server.
6. In Discord, enable **Developer Mode** (User Settings → Advanced), then right-click the channel you want the verse posted in → **Copy Channel ID**. This is your `CHANNEL_ID`.

## 2. Configure

Copy `.env.example` to `.env` and fill in your values:

```
DISCORD_TOKEN=your_bot_token_here
CHANNEL_ID=123456789012345678
TRANSLATION=kjv
POST_HOUR=9
```

## 3. Test locally (optional but recommended)

```bash
pip install -r requirements.txt
python test_verses.py   # confirms every verse reference resolves correctly
python bot.py            # runs the bot; check it logs in and connects
```

The bot checks every minute whether it's past 9:00 AM Eastern and hasn't
posted yet today — if you want to see a post happen without waiting until
9am, temporarily set `POST_HOUR=0` in `.env` and run it.

## 4. Deploy to Railway (free host)

1. Push this folder to a new GitHub repo.
2. Go to [railway.app](https://railway.app) → **New Project** → **Deploy from GitHub repo** → select your repo.
3. Railway will detect the `Procfile` and run it as a worker. If it doesn't auto-detect, set the **Start Command** manually to `python bot.py`.
4. In the project's **Variables** tab, add `DISCORD_TOKEN`, `CHANNEL_ID`, and optionally `TRANSLATION` / `POST_HOUR` (same names/values as your `.env`).
5. Deploy. Check the **Deploy Logs** for `[verse-bot] Logged in as ...` to confirm it's running.

(Render works the same way — "Background Worker" service type, same start command and environment variables.)

## How the daily posting + no-repeat cycle works

- `verses.py` holds the list of verse references.
- On first run, the bot shuffles the whole list into `state.json` as a queue.
- Each day at (or after) 9:00 AM Eastern, it pops the next verse off that
  queue, fetches its text, and posts it. Once the queue is empty it
  reshuffles a fresh full cycle — so you get all 329 verses in a random
  order before anything repeats.
- `state.json` also tracks the last date it posted, so it won't double-post
  if the bot restarts. If the bot happens to be offline at 9am and comes
  back online later that day, it will post as soon as it's back up (once
  per day, never skipped or doubled).

**Note on free hosting:** Railway/Render free tiers can restart or redeploy
your service periodically. `state.json` lives on the container's local
disk, so a full redeploy could reset the cycle progress (you'd just get a
fresh reshuffle, not a crash) — the daily posting itself won't be
disrupted. If you want the cycle position to survive redeploys, ask and I
can wire it up to a persistent volume or a tiny external store.

## Customizing

- **Add/remove verses:** edit the `VERSES` list in `verses.py`, then rerun `python test_verses.py` to confirm the new entries resolve.
- **Change translation:** set `TRANSLATION` in `.env` to any code bible-api.com supports (e.g. `web`, `kjv`, `oeb-us`, `bbe`).
- **Change post time:** set `POST_HOUR` in `.env` (24-hour, Eastern Time).
- **Change the look:** edit the `discord.Embed(...)` block in `bot.py` (title, color, etc.).
