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
