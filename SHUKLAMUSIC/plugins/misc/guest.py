# -----------------------------------------------
# 🔸 StrangerMusic — Guest Banner Feature
# 🔹 User kisi ka @username bheje → bot us user ka stylish banner bheje
# Usage: /banner @username  OR  /tag @username
# -----------------------------------------------
from pyrogram import filters
from pyrogram.enums import ButtonStyle
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from SHUKLAMUSIC import app
import config
from config import BANNED_USERS


# ── Banner text template ──────────────────────────────────────────────────────
def make_banner_text(display_name: str, username: str) -> str:
    mention_link = f"https://t.me/{username}" if username else "#"
    return (
        "╔══════════════════════════════╗\n"
        "║  🎵  <b>𝑴𝑰𝑵𝑻𝑻𝑼𝑵𝑬 𝑴𝑼𝑺𝑰𝑪 𝑩𝑶𝑻</b>  ║\n"
        "╚══════════════════════════════╝\n\n"
        f"❖ <a href=\"{mention_link}\">˹ {display_name} ˼</a> — "
        "<b>𝒀𝒐𝒖𝒓 𝑷𝒓𝒆𝒎𝒊𝒖𝒎 𝑴𝒖𝒔𝒊𝒄 𝑺𝒕𝒓𝒆𝒂𝒎 𝑩𝒐𝒕 🍂</b>\n\n"
        "<blockquote>"
        "🟢 <b>𝑭𝒂𝒔𝒕  •  𝑳𝒂𝒈 𝑭𝒓𝒆𝒆  •  𝑵𝒐 𝑨𝒅𝒔 🍂</b>\n"
        "🎵 <b>𝑨𝒖𝒅𝒊𝒐  •  𝑽𝒊𝒅𝒆𝒐  •  𝑳𝒊𝒗𝒆 𝑺𝒕𝒓𝒆𝒂𝒎 🎥</b>\n"
        "🔄 <b>𝑺𝒑𝒐𝒕𝒊𝒇𝒚 𝑨𝒖𝒕𝒐𝒑𝒍𝒂𝒚  •  𝑴𝒐𝒐𝒅 𝑷𝒍𝒂𝒚𝒍𝒊𝒔𝒕 🎭</b>\n"
        "📚 <b>𝑭𝒐𝒄𝒖𝒔  •  𝑺𝒕𝒖𝒅𝒚  •  𝑪𝒉𝒊𝒍𝒍 𝑴𝒐𝒅𝒆𝒔 🎯</b>"
        "</blockquote>\n\n"
        "◼️ <b>𝑻𝒂𝒑 𝑩𝒆𝒍𝒐𝒘 𝑻𝒐 𝑨𝒅𝒅 𝑴𝒆 𝑰𝒏 𝒀𝒐𝒖𝒓 𝑮𝒓𝒐𝒖𝒑 ✨</b>\n"
        "🎶 <i>𝑬𝒏𝒋𝒐𝒚 𝑯𝒊𝒈𝒉 𝑸𝒖𝒂𝒍𝒊𝒕𝒚 𝑴𝒖𝒔𝒊𝒄 𝑭𝒐𝒓 𝑭𝒓𝒆𝒆 ❄️</i>"
    )


# ── Buttons: Add + Support + Channel ─────────────────────────────────────────
def make_banner_markup(bot_username: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="➕ 𝑨𝒅𝒅 𝑴𝒆 𝑻𝒐 𝒀𝒐𝒖𝒓 𝑮𝒓𝒐𝒖𝒑 ➕",
                    url=f"https://t.me/{bot_username}?startgroup=true",
                    style=ButtonStyle.SUCCESS,
                )
            ],
            [
                InlineKeyboardButton(
                    text="💬 𝑺𝒖𝒑𝒑𝒐𝒓𝒕",
                    url=config.SUPPORT_CHAT,
                    style=ButtonStyle.PRIMARY,
                ),
                InlineKeyboardButton(
                    text="📢 𝑼𝒑𝒅𝒂𝒕𝒆𝒔",
                    url=config.SUPPORT_CHANNEL,
                    style=ButtonStyle.DANGER,
                ),
            ],
        ]
    )


# ──────────────────────────────────────────────────────────────────────────────
# /banner @username  OR  /tag @username
# Koi bhi user ye command bheje — bot us username ka stylish banner send kare
# ──────────────────────────────────────────────────────────────────────────────
@app.on_message(
    filters.command(["banner", "tag", "promo", "share"],
                    prefixes=["/", "!", ".", ","])
    & ~BANNED_USERS
)
async def banner_command(client, message: Message):
    # ── Username extract karo ─────────────────────────────────────────────────
    username = None
    display_name = None

    # Case 1: Reply to someone → unka naam/username lo
    if message.reply_to_message and message.reply_to_message.from_user:
        user = message.reply_to_message.from_user
        username = user.username or ""
        fn = user.first_name or ""
        ln = user.last_name or ""
        display_name = f"{fn} {ln}".strip() or username or "User"

    # Case 2: Command ke saath @username diya
    elif len(message.command) > 1:
        raw = message.command[1].lstrip("@")
        username = raw
        # Try to resolve actual name from Telegram
        try:
            user = await client.get_users(raw)
            fn = user.first_name or ""
            ln = user.last_name or ""
            display_name = f"{fn} {ln}".strip() or raw
            username = user.username or raw
        except Exception:
            display_name = raw  # fallback: username hi naam

    # Case 3: Kuch nahi diya — bot ki info use karo (self banner)
    else:
        me = await client.get_me()
        username = me.username or ""
        fn = me.first_name or ""
        ln = me.last_name or ""
        display_name = f"{fn} {ln}".strip() or "Music Bot"

    # ── Bot ka username buttons ke liye ──────────────────────────────────────
    me = await client.get_me()
    bot_username = me.username or ""

    # ── Banner bhejo ─────────────────────────────────────────────────────────
    banner_text = make_banner_text(display_name, username)
    markup = make_banner_markup(bot_username)

    # NOTE: message.delete() NAHI karte — delete ke baad reply nahi hoti
    # Seedha chat mein send karte hain
    try:
        await client.send_photo(
            chat_id=message.chat.id,
            photo=config.START_IMG_URL,
            caption=banner_text,
            reply_markup=markup,
        )
        # Command message delete karo BAAD mein
        try:
            await message.delete()
        except Exception:
            pass
    except Exception:
        # Photo fail → text only
        try:
            await client.send_message(
                chat_id=message.chat.id,
                text=banner_text,
                reply_markup=markup,
                disable_web_page_preview=True,
            )
            try:
                await message.delete()
            except Exception:
                pass
        except Exception as e:
            print(f"[BANNER ERROR] {type(e).__name__}: {e}")
