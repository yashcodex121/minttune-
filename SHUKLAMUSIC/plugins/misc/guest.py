from pyrogram.enums import ButtonStyle
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InputTextMessageContent,
    Message,
)
from SHUKLAMUSIC import app
import config

# ════════════════════════════════════════
# NOTE: Enable Guest Mode in BotFather:
# BotFather Mini App -> your bot
# -> Bot Settings -> Guest Mode -> Enable
# ════════════════════════════════════════

ADD_ME_PROMO_TEXT = (
    "❖ <a href=\"https://t.me/{username}\">˹{name}˼ ♪</a> — "
    "<b>𝒀𝒐𝒖𝒓 𝑷𝒓𝒆𝒎𝒊𝒖𝒎 𝑴𝒖𝒔𝒊𝒄 𝑺𝒕𝒓𝒆𝒂𝒎 𝑩𝒐𝒕 🍂</b>\n\n"
    "<blockquote>"
    "<b>▸ 𝑭𝒂𝒔𝒕 • 𝑳𝒂𝒈 𝑭𝒓𝒆𝒆 • 𝑵𝒐 𝑨𝒅𝒔 🍂</b>\n"
    "<b>▸ 𝑨𝒖𝒕𝒐-𝑷𝒍𝒂𝒚 • 𝑨𝒖𝒅𝒊𝒐 • 𝑽𝒊𝒅𝒆𝒐 🎥</b>\n"
    "<b>▸ 𝑴𝒐𝒐𝒅 𝑷𝒍𝒂𝒚𝒍𝒊𝒔𝒕 • 𝑺𝒑𝒐𝒕𝒊𝒇𝒚 𝑨𝒖𝒕𝒐𝒑𝒍𝒂𝒚 🎵</b>"
    "</blockquote>\n\n"
    "<b>◼️ 𝑻𝒂𝒑 𝑻𝒉𝒆 𝑩𝒖𝒕𝒕𝒐𝒏 𝑩𝒆𝒍𝒐𝒘 𝑻𝒐 𝑨𝒅𝒅 𝑴𝒆 𝑰𝒏 𝒀𝒐𝒖𝒓 𝑮𝒓𝒐𝒖𝒑 & 𝑬𝒏𝒋𝒐𝒚 𝑯𝒊𝒈𝒉 𝑸𝒖𝒂𝒍𝒊𝒕𝒚 𝑺𝒐𝒏𝒈𝒔 ❄️</b>"
)


def _add_me_markup() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text="✙ 𝑨𝒅𝒅 𝑴𝒆 𝑻𝒐 𝒀𝒐𝒖𝒓 𝑮𝒓𝒐𝒖𝒑 ✙",
                url=f"https://t.me/{app.username}?startgroup=true",
                style=ButtonStyle.SUCCESS,
            )
        ],
        [
            InlineKeyboardButton(
                text="💬 𝑺𝒖𝒑𝒑𝒐𝒓𝒕 𝑪𝒉𝒂𝒕",
                url=config.SUPPORT_CHAT,
                style=ButtonStyle.PRIMARY,
            ),
            InlineKeyboardButton(
                text="📢 𝑼𝒑𝒅𝒂𝒕𝒆𝒔",
                url=config.SUPPORT_CHANNEL,
                style=ButtonStyle.PRIMARY,
            ),
        ],
    ])


async def _build_promo_text() -> str:
    me = await app.get_me()
    name = me.first_name or "Music Bot"
    if me.last_name:
        name = f"{name} {me.last_name}"
    username = me.username or app.username or ""
    return ADD_ME_PROMO_TEXT.format(name=name, username=username), username


@app.on_guest_message()
async def guest_username_mention(_, message: Message):
    if not message.guest_query_id:
        return
    try:
        promo_text, username = await _build_promo_text()
        result = InlineQueryResultArticle(
            title=f"❖ {app.username} ♪",
            description="Tap to send the Add Me card in this chat 🎵",
            thumb_url="https://files.catbox.moe/qv2ob4.jpg",
            input_message_content=InputTextMessageContent(
                message_text=promo_text,
                disable_web_page_preview=True,
            ),
            reply_markup=_add_me_markup(),
        )
        await app.answer_guest_query(message.guest_query_id, result=result)
    except Exception as e:
        print(f"[GUEST ERROR] {type(e).__name__}: {e}")