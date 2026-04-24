# 📨 Telegram Bulk Messenger — Python

Send the same message to **unlimited Telegram users simultaneously** using the official Telegram API. No bans. No third-party services. No cost.

Built with [Telethon](https://github.com/LonamiWebs/Telethon) — the most trusted Python library for the official Telegram MTProto API.

---

## ✨ Features

- ⚡ **Simultaneous delivery** — sends to all recipients at once using async
- 👤 **Flexible recipients** — accepts Telegram usernames (`@handle`) and phone numbers (`+91xxxxxxxxxx`)
- 📝 **Rich formatting** — supports Telegram Markdown and HTML in messages
- 🔁 **Auto flood-wait handling** — if Telegram rate-limits you, the script waits and retries automatically
- 📊 **Live delivery report** — see success, failed, and skipped counts after every run
- 🔒 **Official API** — uses Telegram's MTProto protocol, not a web scraper or bot
- 🚫 **Zero dependencies beyond Telethon** — one `pip install` and you're ready

---

## 📁 File Structure

```
telegram-bulk-messenger/
│
├── telegram_messenger.py   # Main script — edit this
├── requirements.txt        # Python dependencies
├── .gitignore              # Keeps your session file private
└── README.md               # This file
```

---

## ⚙️ Requirements

- Python 3.7+
- A Telegram account (personal account works fine)
- Telegram API credentials (free, takes 2 minutes)

---

## 🚀 Setup & Usage

### Step 1 — Clone the repo

```bash
git clone https://github.com/hi0499954-hue/telegram-bulk-messenger.git
cd telegram-bulk-messenger
```

### Step 2 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 3 — Get your Telegram API credentials

1. Go to 👉 [https://my.telegram.org/auth](https://my.telegram.org/auth)
2. Log in with your Telegram phone number
3. Click **"API Development Tools"**
4. Fill in any app name and click **Create**
5. Copy your **`api_id`** (a number) and **`api_hash`** (a string)

### Step 4 — Configure the script

Open `telegram_messenger.py` and fill in your details:

```python
# Your API credentials from my.telegram.org
API_ID   = 12345678                        # integer, no quotes
API_HASH = "a1b2c3d4e5f6a1b2c3d4e5f6..."  # string, with quotes

# Recipients — mix of usernames and phone numbers
RECIPIENTS = [
    "@username1",
    "@username2",
    "+911234567890",
    "+919876543210",
    # Add as many as you want
]

# Your message — supports **bold**, __italic__, `code`
MESSAGE = """
👋 Hello!

Your message goes here.

Best regards,
Your Name
"""
```

### Step 5 — Run it

```bash
python telegram_messenger.py
```

**First run:** Telegram will ask for your phone number and a verification code sent to your Telegram app. This is a one-time login — after that, a `telegram_session.session` file is created and you stay logged in automatically.

### Step 6 — Watch the live output

```
════════════════════════════════════════════════════════════
   📨  TELEGRAM BULK MESSENGER
════════════════════════════════════════════════════════════
   Recipients : 10
   Time       : 2026-04-14 14:32:01
════════════════════════════════════════════════════════════

  🔗 Connected to Telegram successfully!

  📤 Sending to 10 recipients...

  ✅ Sent → @username1
  ✅ Sent → @username2
  ✅ Sent → +911234567890
  ⚠️  Skipped @username4 → Privacy settings block DMs
  ✅ Sent → @username5
  ...

════════════════════════════════════════════════════════════
   📊  DELIVERY SUMMARY
════════════════════════════════════════════════════════════
   ✅ Sent successfully : 9
   ❌ Failed            : 0
   ⚠️  Skipped          : 1
════════════════════════════════════════════════════════════
```

---

## 📋 Message Formatting

Telegram supports rich text formatting in messages:

| Format | Syntax | Result |
|--------|--------|--------|
| Bold | `**text**` | **text** |
| Italic | `__text__` | _text_ |
| Code | `` `text` `` | `text` |
| Link | `[label](url)` | [label](url) |
| Strikethrough | `~~text~~` | ~~text~~ |

Switch between Markdown and HTML by changing:
```python
PARSE_MODE = "md"    # Markdown (default)
PARSE_MODE = "html"  # HTML tags like <b>, <i>, <code>
```

---

## ⚠️ Error Handling

The script handles all common Telegram errors automatically:

| Error | What happens |
|-------|-------------|
| `FloodWaitError` | Script sleeps for required time, then retries |
| `UserPrivacyRestrictedError` | Recipient has DMs off — logged as Skipped |
| `UsernameNotOccupiedError` | Username doesn't exist — logged as Failed |
| `PeerFloodError` | Too many messages sent recently — logged as Failed |

---

## 🔐 Security Notes

- **Never share your `.session` file** — it contains your Telegram login. The `.gitignore` already excludes it from Git.
- **Never share your `api_hash`** — treat it like a password. Consider using environment variables for production:

```python
import os
API_ID   = int(os.environ.get("TELEGRAM_API_ID"))
API_HASH = os.environ.get("TELEGRAM_API_HASH")
```

```bash
# Set before running
export TELEGRAM_API_ID=12345678
export TELEGRAM_API_HASH=a1b2c3d4e5f6...
```

---

## 🆚 Why Telegram over WhatsApp or Instagram?

| Feature | Telegram ✅ | WhatsApp ⚠️ | Instagram ❌ |
|---------|------------|------------|-------------|
| Official API | ✅ Free | ❌ Paid + approval | ❌ None |
| Bulk messaging | ✅ Supported | ❌ Banned | ❌ Banned |
| No account bans | ✅ | ❌ High risk | ❌ Instant ban |
| Python library | ✅ Telethon | ⚠️ Unofficial only | ❌ None |
| Live demo safe | ✅ | ❌ | ❌ |

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 🙋 Author

Built for a college competition on creative integrations.
Uses Python's `asyncio` + Telegram's official MTProto API via Telethon.
