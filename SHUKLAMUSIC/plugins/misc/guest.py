# -----------------------------------------------
# 🔸 StrangerMusic Project — Guest / Promo Feature
# 🔹 /addme command + inline share card
# -----------------------------------------------
from pyrogram import filters
from pyrogram.enums import ButtonStyle
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
    Message,
)
from SHUKLAMUSIC import app
import config
from config import BANNED_USERS


# ── Promo message text ────────────────────────────────────────────────────────
PROMO_TEXT = (
    "╔══════════════════════════════╗\n"
    "║  🎵  <b>𝑴𝑰𝑵𝑻𝑻𝑼𝑵𝑬 𝑴𝑼𝑺𝑰𝑪 𝑩𝑶𝑻</b>  ║\n"
    "╚══════════════════════════════╝\n\n"
    "❖ <a href=\"https://t.me/{username}\">˹ {name} ˼</a> — "
    "<b>𝒀𝒐𝒖𝒓 𝑷𝒓𝒆𝒎𝒊𝒖𝒎 𝑴𝒖𝒔𝒊𝒄 𝑺𝒕𝒓𝒆𝒂𝒎 𝑩𝒐𝒕 🍂</b>\n\n"
    "<blockquote>"
    "🟢 <b>𝑭𝒂𝒔𝒕  •  𝑳𝒂𝒈 𝑭𝒓𝒆𝒆  •  𝑵𝒐 𝑨𝒅𝒔 🍂</b>\n"
    "🎵 <b>𝑨𝒖𝒅𝒊𝒐  •  𝑽𝒊𝒅𝒆𝒐  •  𝑳𝒊𝒗𝒆 𝑺𝒕𝒓𝒆𝒂𝒎 🎥</b>\n"
    "🔄 <b>𝑺𝒑𝒐𝒕𝒊𝒇𝒚 𝑨𝒖𝒕𝒐𝒑𝒍𝒂𝒚  •  𝑴𝒐𝒐𝒅 𝑷𝒍𝒂𝒚𝒍𝒊𝒔𝒕 🎭</b>\n"
    "📚 <b>𝑭𝒐𝒄𝒖𝒔  •  𝑺𝒕𝒖𝒅𝒚  •  𝑪𝒉𝒊𝒍𝒍 𝑴𝒐𝒅𝒆𝒔 🎯</b>"
    "</blockquote>\n\n"
    "◼️ <b>𝑻𝒂𝒑 𝑻𝒉𝒆 𝑩𝒖𝒕𝒕𝒐𝒏 𝑩𝒆𝒍𝒐𝒘 𝑻𝒐 𝑨𝒅𝒅 𝑴𝒆 𝑰𝒏 𝒀𝒐𝒖𝒓 𝑮𝒓𝒐𝒖𝒑</b>\n"
    "🎶 <i>𝑬𝒏𝒋𝒐𝒚 𝑯𝒊𝒈𝒉 𝑸𝒖𝒂𝒍𝒊𝒕𝒚 𝑴𝒖𝒔𝒊𝒄 𝑭𝒐𝒓 𝑭𝒓𝒆𝒆 ❄️</i>"
)


# ── Inline keyboard: Add + Support (colorful) ─────────────────────────────────
def _add_me_markup(username: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="➕ 𝑨𝒅𝒅 𝑴𝒆 𝑻𝒐 𝒀𝒐𝒖𝒓 𝑮𝒓𝒐𝒖𝒑 ➕",
                    url=f"https://t.me/{username}?startgroup=true",
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


# ── Helper: build promo text + get bot info ───────────────────────────────────
async def _build_promo() -> tuple:
    me = await app.get_me()
    name = me.first_name or "Music Bot"
    if me.last_name:
        name = f"{name} {me.last_name}"
    username = me.username or ""
    text = PROMO_TEXT.format(name=name, username=username)
    return text, username, name


# ──────────────────────────────────────────────────────────────────────────────
# /addme command — sends the promo card directly in chat
# ──────────────────────────────────────────────────────────────────────────────
@app.on_message(
    filters.command(["addme", "invite", "add"], prefixes=["/", "!", ".", ","])
    & ~BANNED_USERS
)
async def addme_command(client, message: Message):
    try:
        await message.delete()
    except Exception:
        pass
    try:
        promo_text, username, name = await _build_promo()
        await message.reply_photo(
            photo=config.START_IMG_URL,
            caption=promo_text,
            reply_markup=_add_me_markup(username),
        )
    except Exception:
        # Fallback: text only if photo fails
        try:
            promo_text, username, name = await _build_promo()
            await message.reply_text(
                promo_text,
                reply_markup=_add_me_markup(username),
                disable_web_page_preview=True,
            )
        except Exception as e:
            print(f"[ADDME ERROR] {type(e).__name__}: {e}")


# ──────────────────────────────────────────────────────────────────────────────
# Inline query — type @botname in any chat to share the promo card
# ──────────────────────────────────────────────────────────────────────────────
@app.on_inline_query(filters.regex(r"^(add|invite|share|music)?$", flags=2))
async def inline_addme(client, inline_query: InlineQuery):
    try:
        promo_text, username, name = await _build_promo()
        results = [
            InlineQueryResultArticle(
                title=f"🎵 Add {name} to your group",
                description="Tap to share the Add Me card in any chat",
                thumb_url=config.START_IMG_URL,
                input_message_content=InputTextMessageContent(
                    message_text=promo_text,
                    disable_web_page_preview=True,
                ),
                reply_markup=_add_me_markup(username),
            )
        ]
        await inline_query.answer(
            results=results,
            cache_time=30,
            is_personal=False,
        )
    except Exception as e:
        print(f"[INLINE GUEST ERROR] {type(e).__name__}: {e}")
