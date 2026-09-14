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

## 4. Deploy to Oracle Cloud Free Tier (your own VM, dedicated IP)

This runs the bot on a real, always-on virtual machine that's yours alone —
no shared IP with other people's apps, which avoids the Discord/Cloudflare
rate-limit blocks that shared-IP platforms (Render, Railway, etc. free
tiers) can run into.

**4a. Create the VM**
1. Sign up at [cloud.oracle.com](https://cloud.oracle.com) (requires a credit card for identity verification, but the Always Free resources never charge it).
2. Once in the console: **Compute** → **Instances** → **Create Instance**.
3. Name it anything. Under **Image and shape**, pick an **Always Free eligible** shape (Ampere A1 or VM.Standard.E2.1.Micro) — the console labels these clearly.
4. Under **Add SSH keys**, choose "Generate a key pair" and **download the private key** — you'll need it to log in.
5. Leave networking on defaults and click **Create**. Wait for it to show "Running," then copy its **Public IP Address**.

**4b. Connect and set up the server**

From PowerShell (or any terminal), SSH in using the key you downloaded:

```powershell
ssh -i "path\to\your-downloaded-key.key" ubuntu@YOUR_PUBLIC_IP
```

(Username is `ubuntu` for Ubuntu images, `opc` for Oracle Linux images.)

Once connected, install what you need:

```bash
sudo apt update && sudo apt install -y python3 python3-venv python3-pip git
```

**4c. Get your code onto the VM**

Easiest path — clone straight from your GitHub repo:

```bash
git clone https://github.com/YOUR_USERNAME/discord-verse-bot.git
cd discord-verse-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**4d. Configure**

```bash
cp .env.example .env
nano .env
```

Fill in your real `DISCORD_TOKEN` and `CHANNEL_ID`, then save (Ctrl+O, Enter, Ctrl+X in nano).

**4e. Test it**

```bash
python test_verses.py
python bot.py
```

Confirm you see "Logged in as..." then stop it with Ctrl+C.

**4f. Run it 24/7 with systemd**

This repo includes `discord-verse-bot.service`, which keeps the bot running
permanently and auto-restarts it if it ever crashes or the VM reboots.

```bash
sudo cp discord-verse-bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable discord-verse-bot
sudo systemctl start discord-verse-bot
```

Check it's running and see live logs:

```bash
sudo systemctl status discord-verse-bot
journalctl -u discord-verse-bot -f
```

That's it — the bot now runs continuously on a dedicated IP, survives
reboots, and restarts itself if it ever crashes.

### <details><summary>Alternative: Render free Web Service (click to expand)</summary>

Render's free tier only offers "Web Service" instances (not "Background
Worker"), and Web Services expect HTTP traffic or they spin down after ~15
minutes of inactivity. If you go this route instead of a VM, you'd need to
add back a tiny built-in web server to `bot.py` (ask and I can provide it)
and pair it with a free [UptimeRobot](https://uptimerobot.com) monitor
pinging the service every few minutes to keep it awake. Note: Render's free
tier uses shared outbound IPs, which can occasionally get temporarily
blocked by Discord/Cloudflare if other free-tier apps on the same IP get
flagged for abuse — this is the exact problem the Oracle Cloud VM approach
above avoids.

</details>

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

## Customizing

- **Add/remove verses:** edit the `VERSES` list in `verses.py`, then rerun `python test_verses.py` to confirm the new entries resolve.
- **Change translation:** set `TRANSLATION` in `.env` to any code bible-api.com supports (e.g. `web`, `kjv`, `oeb-us`, `bbe`).
- **Change post time:** set `POST_HOUR` in `.env` (24-hour, Eastern Time).
- **Change the look:** edit the `discord.Embed(...)` block in `bot.py` (title, color, etc.).
- **Update the code later:** on the VM, `cd discord-verse-bot && git pull && sudo systemctl restart discord-verse-bot`.

