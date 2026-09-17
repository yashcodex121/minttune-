# -----------------------------------------------
# 🔸 StrangerMusic — Guest Banner Feature
# Usage:
#   /banner @username   — kisi ka username deke banner bhejo
#   /banner             — reply karte hue banner bhejo
#   /banner             — kuch nahi diya → bot ka apna banner
# -----------------------------------------------
from pyrogram import filters
from pyrogram.enums import ButtonStyle, ParseMode
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from SHUKLAMUSIC import app
import config
from config import BANNED_USERS

BANNER_IMG = "https://files.catbox.moe/qv2ob4.jpg"


def make_banner_text(display_name: str, username: str) -> str:
    if username:
        name_part = f'<a href="https://t.me/{username}">˹ {display_name} ˼</a>'
    else:
        name_part = f"˹ {display_name} ˼"
    return (
        "╔══════════════════════════════╗\n"
        "║  🎵  <b>𝑴𝑰𝑵𝑻𝑻𝑼𝑵𝑬 𝑴𝑼𝑺𝑰𝑪 𝑩𝑶𝑻</b>  ║\n"
        "╚══════════════════════════════╝\n\n"
        f"❖ {name_part} — <b>𝒀𝒐𝒖𝒓 𝑷𝒓𝒆𝒎𝒊𝒖𝒎 𝑴𝒖𝒔𝒊𝒄 𝑺𝒕𝒓𝒆𝒂𝒎 𝑩𝒐𝒕 🍂</b>\n\n"
        "<blockquote>"
        "🟢 <b>𝑭𝒂𝒔𝒕  •  𝑳𝒂𝒈 𝑭𝒓𝒆𝒆  •  𝑵𝒐 𝑨𝒅𝒔 🍂</b>\n"
        "🎵 <b>𝑨𝒖𝒅𝒊𝒐  •  𝑽𝒊𝒅𝒆𝒐  •  𝑳𝒊𝒗𝒆 𝑺𝒕𝒓𝒆𝒂𝒎 🎥</b>\n"
        "🔄 <b>𝑺𝒑𝒐𝒕𝒊𝒇𝒚 𝑨𝒖𝒕𝒐𝒑𝒍𝒂𝒚  •  𝑴𝒐𝒐𝒅 𝑷𝒍𝒂𝒚𝒍𝒊𝒔𝒕 🎭</b>\n"
        "📚 <b>𝑭𝒐𝒄𝒖𝒔  •  𝑺𝒕𝒖𝒅𝒚  •  𝑪𝒉𝒊𝒍𝒍 𝑴𝒐𝒅𝒆𝒔 🎯</b>"
        "</blockquote>\n\n"
        "◼️ <b>𝑻𝒂𝒑 𝑩𝒆𝒍𝒐𝒘 𝑻𝒐 𝑨𝒅𝒅 𝑴𝒆 𝑰𝒏 𝒀𝒐𝒖𝒓 𝑮𝒓𝒐𝒖𝒑 ✨</b>\n"
        "🎶 <i>𝑬𝒏𝒋𝒐𝒚 𝑯𝒊𝒈𝒉 𝑸𝒖𝒂𝒍𝒊𝒕𝒚 𝑴𝒖𝒔𝒊𝒄 𝑭𝒐𝒓 𝑭𝒓𝒆𝒆 ❄️</i>"
    )


def make_banner_markup(bot_username: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
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
    ])


@app.on_message(
    filters.command(["banner", "tag", "promo", "share"],
                    prefixes=["/", "!", ".", ","])
    & ~BANNED_USERS
)
async def banner_command(client, message: Message):

    # ── Resolve name + username ───────────────────────────────────────────────
    display_name = ""
    username = ""

    if message.reply_to_message and message.reply_to_message.from_user:
        u = message.reply_to_message.from_user
        username = u.username or ""
        display_name = f"{u.first_name or ''} {u.last_name or ''}".strip() or username or "User"

    elif len(message.command) > 1:
        raw = message.command[1].strip().lstrip("@")
        username = raw
        display_name = raw
        try:
            u = await client.get_users(raw)
            username = u.username or raw
            display_name = f"{u.first_name or ''} {u.last_name or ''}".strip() or raw
        except Exception as e:
            print(f"[BANNER] get_users('{raw}') failed: {e}")

    else:
        me = await client.get_me()
        username = me.username or ""
        display_name = f"{me.first_name or ''} {me.last_name or ''}".strip() or "Music Bot"

    # ── Bot username ──────────────────────────────────────────────────────────
    try:
        me = await client.get_me()
        bot_username = me.username or ""
    except Exception:
        bot_username = ""

    caption = make_banner_text(display_name, username)
    markup  = make_banner_markup(bot_username)

    # ── Send — try photo, fallback text ──────────────────────────────────────
    try:
        await message.reply_photo(
            photo=BANNER_IMG,
            caption=caption,
            reply_markup=markup,
            parse_mode=ParseMode.HTML,
        )
        try:
            await message.delete()
        except Exception:
            pass
        return
    except Exception as e:
        print(f"[BANNER] reply_photo failed: {type(e).__name__}: {e}")

    try:
        await message.reply_text(
            text=caption,
            reply_markup=markup,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
        )
        try:
            await message.delete()
        except Exception:
            pass
    except Exception as e:
        print(f"[BANNER] reply_text also failed: {type(e).__name__}: {e}")
        await message.reply_text("❌ Banner send nahi ho saka. Check logs.")
