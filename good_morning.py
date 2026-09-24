"""Daily "good morning": posts MESSAGE to a Discord channel using your own
account token. Waits until SEND_TIME (in TIMEZONE) before sending.

WARNING: automating a user account is against Discord's Terms of Service and
can get the account banned. The token gives full access to your account -
keep it only in a GitHub secret, never in code."""
import datetime as dt
import json
import os
import random
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from zoneinfo import ZoneInfo

TOKEN = os.environ.get("DISCORD_TOKEN", "").strip()
CHANNEL = os.environ.get("DISCORD_CHANNEL", "").strip()
MESSAGE = os.environ.get("MESSAGE", "").strip() or (
    "/book character:Druid Fireblade spot:Nightmare Isle "
    "date:24.09.2026 start:03:00 end:06:00"
)
# Optional: after the message, also post a Tenor GIF for this search (like /gif query:...).
GIF_QUERY = os.environ.get("GIF_QUERY", "").strip()
SEND_TIME = os.environ.get("SEND_TIME", "").strip() or "08:00"
TIMEZONE = os.environ.get("TIMEZONE", "").strip() or "Europe/Warsaw"
# Cron that started this run, e.g. "30 5 * * *" (empty for manual runs).
SCHEDULE = os.environ.get("SCHEDULE", "").strip()


def channel_id(value):
    """Accepts a channel ID or a link like discord.com/channels/<guild>/<channel>."""
    m = re.search(r"channels/(?:@me|\d+)/(\d+)", value)
    if m:
        return m.group(1)
    if value.isdigit():
        return value
    sys.exit(f"DISCORD_CHANNEL is not a channel ID or link: {value!r}")


def target_today():
    tz = ZoneInfo(TIMEZONE)
    hour, minute = map(int, SEND_TIME.split(":"))
    now = dt.datetime.now(tz)
    return now.replace(hour=hour, minute=minute, second=0, microsecond=0)


def wait_until(target):
    while True:
        left = (target - dt.datetime.now(dt.timezone.utc)).total_seconds()
        if left <= 0:
            return
        if left > 60:
            print(f"{left:.0f}s left", flush=True)
        time.sleep(min(left, 30))


def find_gif(query):
    """Returns a random tenor.com GIF link for the search; Discord embeds it as a GIF."""
    slug = urllib.parse.quote(re.sub(r"\s+", "-", query.strip().lower()))
    req = urllib.request.Request(f"https://tenor.com/search/{slug}-gifs",
                                 headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        html = r.read().decode("utf-8", "replace")
    links = sorted(set(re.findall(r"/view/[\w-]+-gif-\d+", html)))
    if not links:
        sys.exit(f"No GIFs found on Tenor for {query!r}")
    return "https://tenor.com" + random.choice(links[:20])


def send(cid, text):
    req = urllib.request.Request(
        f"https://discord.com/api/v9/channels/{cid}/messages",
        data=json.dumps({"content": text}).encode(),
        headers={"Authorization": TOKEN, "Content-Type": "application/json",
                 "User-Agent": "good-morning"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            print(f"Sent to channel {cid} -> {r.status}")
    except urllib.error.HTTPError as e:
        hint = {401: "token is invalid or expired - copy a fresh one",
                403: "no permission to write in that channel",
                404: "channel not found - check DISCORD_CHANNEL"}.get(e.code, "")
        sys.exit(f"Discord refused: {e.code} {e.read()[:200]!r} {hint}")


def main():
    if not TOKEN or not CHANNEL:
        sys.exit("Set DISCORD_TOKEN and DISCORD_CHANNEL secrets.")
    cid = channel_id(CHANNEL)

    if os.environ.get("SEND_NOW") != "true":
        target = target_today()
        if SCHEDULE:
            # Two crons run 1h apart to cover summer/winter time. Only the one
            # that starts ~30 min before SEND_TIME sends; the other exits.
            fired_hour = int(SCHEDULE.split()[1])
            wanted_hour = (target - dt.timedelta(minutes=30)).astimezone(dt.timezone.utc).hour
            if fired_hour != wanted_hour:
                print(f"Not this run's turn (cron hour {fired_hour} UTC, need {wanted_hour}).")
                return
        wait_until(target)

    send(cid, MESSAGE)
    if GIF_QUERY:
        gif = find_gif(GIF_QUERY)
        print("GIF:", gif)
        send(cid, gif)


if __name__ == "__main__":
    main()
