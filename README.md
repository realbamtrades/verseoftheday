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

## 4. Deploy to Render (free Web Service)

Render's free tier only covers "Web Service" instances — not "Background
Worker" — so this bot includes a tiny built-in web server whose only job is
giving Render something to respond to. It doesn't affect the bot's actual
function at all.

1. Push this folder to a GitHub repo.
2. Go to [render.com](https://render.com) → **New +** → **Web Service** (not Background Worker) → connect and select your repo.
3. Settings:
   - Runtime: **Python 3**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python bot.py`
   - Instance Type: **Free**
4. Under **Environment Variables**, add `DISCORD_TOKEN` and `CHANNEL_ID` (and optionally `TRANSLATION` / `POST_HOUR`). Render sets `PORT` automatically — you don't need to add it yourself.
5. Deploy. Check the **Logs** tab for `[verse-bot] Logged in as ...` and `[verse-bot] Health-check web server listening on port ...`.

### Keeping it awake (important)

Render's free Web Services spin down after ~15 minutes with no incoming HTTP
traffic. Your bot doesn't receive HTTP traffic on its own — it only talks
outward to Discord — so without help, Render will eventually treat it as
idle and shut it down, which would silently stop your daily posts.

To prevent that, use a free uptime-monitoring service to ping your Render
URL every few minutes so it never looks idle:

1. Once deployed, copy your service's public URL from the Render dashboard (looks like `https://your-bot-name.onrender.com`).
2. Sign up at [UptimeRobot](https://uptimerobot.com) (free).
3. Add a new monitor: **HTTP(s)**, paste your Render URL, set the check interval to **5 minutes**.
4. Save it. UptimeRobot will now hit your bot's health-check endpoint every 5 minutes, keeping it awake 24/7.

This is a known workaround, not an official Render feature — it's the
tradeoff for using the free tier instead of the paid Starter plan ($7/mo),
which runs Background Workers with no spin-down and no pinging required.

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

**Note on free hosting:** Render's free Web Service tier requires the
keep-alive setup described above (UptimeRobot) or it will spin down and
your bot will go offline until manually restarted or the next deploy. Even
with a pinger running, free tiers can occasionally be less reliable than a
paid instance — if you want zero-maintenance guaranteed uptime, the Starter
plan ($7/month, deployed as a Background Worker instead) removes the need
for the web server trick and the external pinger entirely. Also, `state.json`
lives on the container's local disk, so a full redeploy could reset the
cycle progress (you'd just get a fresh reshuffle, not a crash) — the daily
posting itself won't be disrupted.

## Customizing

- **Add/remove verses:** edit the `VERSES` list in `verses.py`, then rerun `python test_verses.py` to confirm the new entries resolve.
- **Change translation:** set `TRANSLATION` in `.env` to any code bible-api.com supports (e.g. `web`, `kjv`, `oeb-us`, `bbe`).
- **Change post time:** set `POST_HOUR` in `.env` (24-hour, Eastern Time).
- **Change the look:** edit the `discord.Embed(...)` block in `bot.py` (title, color, etc.).
