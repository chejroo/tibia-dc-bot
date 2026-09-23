"""Booking reminder: waits until TARGET_UTC, then sends the /book command
to a Discord webhook and/or an ntfy.sh topic so you can paste it yourself."""
import datetime as dt
import json
import os
import sys
import time
import urllib.request

TARGET_UTC = os.environ.get("TARGET_UTC", "2026-09-24T08:00:00+00:00")  # 10:00 CEST
COMMAND = os.environ.get(
    "BOOK_COMMAND",
    "/book character:Druid Fireblade spot:Book World - Chapter III "
    "date:24.09.2026 start:12:00 end:14:00",
)
WEBHOOK = os.environ.get("DISCORD_WEBHOOK_URL", "").strip()
MENTION = os.environ.get("DISCORD_USER_ID", "").strip()
NTFY_TOPIC = os.environ.get("NTFY_TOPIC", "").strip()


def post(url, data, headers):
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=15) as r:
        print(f"POST {url.split('?')[0][:40]}... -> {r.status}")


def wait_until(target):
    while True:
        left = (target - dt.datetime.now(dt.timezone.utc)).total_seconds()
        if left <= 0:
            return
        if left > 60:
            print(f"{left:.0f}s left", flush=True)
        time.sleep(min(left, 30))


def main():
    if not WEBHOOK and not NTFY_TOPIC:
        sys.exit("Set DISCORD_WEBHOOK_URL and/or NTFY_TOPIC secret.")
    if os.environ.get("SEND_NOW") != "true":
        wait_until(dt.datetime.fromisoformat(TARGET_UTC))

    errors = 0
    if WEBHOOK:
        ping = f"<@{MENTION}> " if MENTION else ""
        body = {
            "content": f"{ping}⏰ Booking time! Paste this now:\n```\n{COMMAND}\n```",
            "allowed_mentions": {"users": [MENTION] if MENTION else []},
        }
        try:
            post(WEBHOOK, json.dumps(body).encode(),
                 {"Content-Type": "application/json", "User-Agent": "booking-reminder"})
        except Exception as e:
            errors += 1
            print("Discord failed:", e)
    if NTFY_TOPIC:
        try:
            post(f"https://ntfy.sh/{NTFY_TOPIC}", COMMAND.encode(),
                 {"Title": "Secura booking - paste now!", "Priority": "urgent",
                  "Tags": "alarm_clock"})
        except Exception as e:
            errors += 1
            print("ntfy failed:", e)
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
