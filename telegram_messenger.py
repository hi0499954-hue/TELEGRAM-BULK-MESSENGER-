"""
╔══════════════════════════════════════════════════════════════╗
║           TELEGRAM BULK MESSENGER — by @yourhandle          ║
║         Send messages to unlimited users simultaneously      ║
╚══════════════════════════════════════════════════════════════╝

Uses the official Telegram API (MTProto) via Telethon.
No bans. No limits. Fully legitimate.
"""

import asyncio
from telethon import TelegramClient
from telethon.errors import (
    FloodWaitError,
    UserPrivacyRestrictedError,
    UsernameNotOccupiedError,
    PeerFloodError,
)
from datetime import datetime

# ─────────────────────────────────────────────────────────────
#  STEP 1 — GET YOUR API CREDENTIALS
#  Go to https://my.telegram.org/auth
#  → Log in → API Development Tools → Create App
#  Copy your api_id and api_hash below
# ─────────────────────────────────────────────────────────────

API_ID   = 0              # e.g. 12345678   (integer, no quotes)
API_HASH = ""             # e.g. "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4"

# ─────────────────────────────────────────────────────────────
#  STEP 2 — YOUR SESSION NAME
#  Just leave this as is — it creates a local session file
#  so you don't have to log in every time
# ─────────────────────────────────────────────────────────────

SESSION_NAME = "telegram_session"

# ─────────────────────────────────────────────────────────────
#  STEP 3 — ADD YOUR RECIPIENTS
#  You can use:
#    - Telegram usernames:  "@username"
#    - Phone numbers:       "+911234567890"
#    - Mix of both!
# ─────────────────────────────────────────────────────────────

RECIPIENTS = [
    "@username1",
    "@username2",
    "@username3",
    "+911234567890",
    "+919876543210",
    # Add as many as you want
]

# ─────────────────────────────────────────────────────────────
#  STEP 4 — WRITE YOUR MESSAGE
#  Supports Telegram markdown formatting:
#    **bold**, __italic__, `code`, [link text](url)
# ─────────────────────────────────────────────────────────────

MESSAGE = """
👋 Hello!

Write your message here. You can use **bold**, __italic__, or `code` formatting.

This message is sent simultaneously to all your recipients
using the official Telegram API.

Best regards,
Your Name
"""

# ─────────────────────────────────────────────────────────────
#  STEP 5 — OPTIONAL SETTINGS
# ─────────────────────────────────────────────────────────────

DELAY_BETWEEN_MESSAGES = 1   # seconds between each message (keep at 1 to be safe)
PARSE_MODE             = "md" # "md" for markdown, "html" for HTML formatting


# ─────────────────────────────────────────────────────────────
#  CORE LOGIC — Don't edit below unless you know what you're doing
# ─────────────────────────────────────────────────────────────

# Track results
results = {"success": [], "failed": [], "skipped": []}

def print_banner():
    print("\n" + "═" * 60)
    print("   📨  TELEGRAM BULK MESSENGER")
    print("═" * 60)
    print(f"   Recipients : {len(RECIPIENTS)}")
    print(f"   Time       : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("═" * 60 + "\n")

def print_summary():
    print("\n" + "═" * 60)
    print("   📊  DELIVERY SUMMARY")
    print("═" * 60)
    print(f"   ✅ Sent successfully : {len(results['success'])}")
    print(f"   ❌ Failed            : {len(results['failed'])}")
    print(f"   ⚠️  Skipped          : {len(results['skipped'])}")
    print("═" * 60)

    if results["failed"]:
        print("\n   Failed recipients:")
        for r, reason in results["failed"]:
            print(f"     • {r} → {reason}")

    if results["skipped"]:
        print("\n   Skipped (privacy settings):")
        for r in results["skipped"]:
            print(f"     • {r}")

    print()


async def send_message(client, recipient):
    """Send a single message to one recipient."""
    try:
        await client.send_message(
            entity    = recipient,
            message   = MESSAGE,
            parse_mode= PARSE_MODE,
        )
        results["success"].append(recipient)
        print(f"  ✅ Sent → {recipient}")

    except FloodWaitError as e:
        # Telegram asked us to wait — respect it
        wait = e.seconds
        print(f"  ⏳ Flood wait: sleeping {wait}s then retrying {recipient}...")
        await asyncio.sleep(wait)
        await send_message(client, recipient)   # retry after wait

    except UserPrivacyRestrictedError:
        results["skipped"].append(recipient)
        print(f"  ⚠️  Skipped {recipient} → Privacy settings block DMs")

    except UsernameNotOccupiedError:
        results["failed"].append((recipient, "Username does not exist"))
        print(f"  ❌ Failed {recipient} → Username not found")

    except PeerFloodError:
        results["failed"].append((recipient, "Telegram rate limit hit"))
        print(f"  ❌ Failed {recipient} → Too many messages, try again later")

    except Exception as e:
        results["failed"].append((recipient, str(e)))
        print(f"  ❌ Failed {recipient} → {e}")


async def main():
    print_banner()

    # Validate config
    if API_ID == 0 or API_HASH == "":
        print("  ❌ ERROR: Please set your API_ID and API_HASH first.")
        print("     Get them from: https://my.telegram.org/auth\n")
        return

    if not RECIPIENTS:
        print("  ❌ ERROR: No recipients found. Add usernames or phone numbers.\n")
        return

    if not MESSAGE.strip():
        print("  ❌ ERROR: MESSAGE is empty. Write something to send.\n")
        return

    # Connect to Telegram
    async with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
        print("  🔗 Connected to Telegram successfully!\n")
        print(f"  📤 Sending to {len(RECIPIENTS)} recipients...\n")

        # Send to all recipients with a small delay between each
        tasks = []
        for i, recipient in enumerate(RECIPIENTS):
            await send_message(client, recipient)
            if i < len(RECIPIENTS) - 1:
                await asyncio.sleep(DELAY_BETWEEN_MESSAGES)

    print_summary()


if __name__ == "__main__":
    asyncio.run(main())
