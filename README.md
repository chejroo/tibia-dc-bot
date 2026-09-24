# Secura booking reminder

At **10:00:00 CEST on 24.09.2026**, this sends you the `/book` command ready to paste:

```
/book character:Druid Fireblade spot:Book World - Chapter III date:24.09.2026 start:12:00 end:14:00
```

## Setup (repo → Settings → Secrets and variables → Actions → New repository secret)

Set at least one of these:

| Secret | What |
|---|---|
| `DISCORD_WEBHOOK_URL` | Webhook of a channel on **your own** server (Channel settings → Integrations → Webhooks → New Webhook → Copy URL) |
| `DISCORD_USER_ID` | Optional: your user ID so the message pings you (Developer Mode → right-click yourself → Copy User ID) |
| `NTFY_TOPIC` | Phone push: install the **ntfy** app, subscribe to a hard-to-guess topic name (e.g. `fireblade-book-8x2k`), put the same name here |

## Test

Actions tab → **Booking reminder** → Run workflow (leave "Send immediately" checked). You should get the message within a minute.

---

# Daily "good morning"

Every day at **08:00 Europe/Warsaw** (CEST/CET handled automatically), `good_morning.py` posts `/book character:Druid Fireblade spot:Nightmare Isle date:24.09.2026 start:03:00 end:06:00` (as plain text) to a channel **from your own account**.

> ⚠️ Automating a user account is against Discord's Terms of Service and can get your account banned. Your token gives full access to your account: keep it only in the secret below, never commit it, and if it leaks, change your password (that invalidates the token).

## Setup (repo → Settings → Secrets and variables → Actions)

| Secret | What |
|---|---|
| `DISCORD_TOKEN` | Your account token |
| `DISCORD_CHANNEL` | Channel link (right-click channel → Copy Link, e.g. `https://discord.com/channels/111/222`) or just the channel ID |

Optional **variables** (Variables tab): `GOOD_MORNING_MESSAGE` to change the text, `GIF_QUERY` (e.g. `hello`) to also post a Tenor GIF after it, like `/gif query:hello`.

Manual runs can also take a one-off message and GIF search.

To change the time, edit `SEND_TIME`/`TIMEZONE` defaults in `good_morning.py` and the two crons in `.github/workflows/good-morning.yml` (they must start ~30 min before the send time, one for summer and one for winter).

## Test

Actions tab → **Good morning** → Run workflow (leave "Send immediately" checked).
