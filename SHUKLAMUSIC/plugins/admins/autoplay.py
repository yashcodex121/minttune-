# -----------------------------------------------
# 🔸 StrangerMusic Project — Autoplay Command
# 🔹 Spotify-style autoplay: plays related songs automatically when queue ends
# -----------------------------------------------
from pyrogram import filters
from pyrogram.enums import ButtonStyle
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from SHUKLAMUSIC import app
from SHUKLAMUSIC.utils.database import (
    get_autoplay,
    set_autoplay,
    set_autoplay_owner,
)
from SHUKLAMUSIC.utils.decorators import AdminRightsCheck
from config import BANNED_USERS


# ── Inline keyboard for autoplay status message ─────────────────────────────
def autoplay_markup(chat_id: int, state: bool) -> InlineKeyboardMarkup:
    if state:
        toggle_text = "🔄 𝑨𝒖𝒕𝒐𝒑𝒍𝒂𝒚 𝑶𝑵  ✅"
        toggle_style = ButtonStyle.SUCCESS
    else:
        toggle_text = "🔄 𝑨𝒖𝒕𝒐𝒑𝒍𝒂𝒚 𝑶𝑭𝑭  ❌"
        toggle_style = ButtonStyle.DANGER

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=toggle_text,
                    callback_data=f"ADMIN Autoplay|{chat_id}",
                    style=toggle_style,
                )
            ],
            [
                InlineKeyboardButton(
                    text="✖️ 𝑪𝒍𝒐𝒔𝒆",
                    callback_data="close",
                    style=ButtonStyle.PRIMARY,
                )
            ],
        ]
    )


# ── Colorful autoplay status text ────────────────────────────────────────────
def autoplay_text(state: bool, mention: str) -> str:
    if state:
        return (
            "◆━━━━━━━━━━━━━━━━━━━◆\n"
            "     🎵 A U T O P L A Y\n"
            "◆━━━━━━━━━━━━━━━━━━━◆\n\n"
            "✨ <b>Status:</b> <code>Enabled ✅</code>\n\n"
            "🎶 <i>Sit back — I'll auto-play related\n"
            "tracks once the queue runs dry!</i>\n\n"
            f"👤 <b>Turned on by:</b> {mention}"
        )
    else:
        return (
            "◆━━━━━━━━━━━━━━━━━━━◆\n"
            "     🎵 A U T O P L A Y\n"
            "◆━━━━━━━━━━━━━━━━━━━◆\n\n"
            "🚫 <b>Status:</b> <code>Disabled ❌</code>\n\n"
            "🎧 <i>No more auto-play — I'll head out\n"
            "once the queue is finished.</i>\n\n"
            f"👤 <b>Turned off by:</b> {mention}"
        )


# ── /autoplay command ─────────────────────────────────────────────────────────
@app.on_message(
    filters.command(["autoplay", "ap"], prefixes=["/", "!", ".", ","])
    & filters.group
    & ~BANNED_USERS
)
@AdminRightsCheck
async def autoplay_command(client, message: Message, _, chat_id):
    mention = message.from_user.mention

    # Current state → toggle it
    current_state = await get_autoplay(chat_id)
    new_state = not current_state
    await set_autoplay(chat_id, new_state)
    if new_state:
        await set_autoplay_owner(chat_id, message.from_user.id)

    try:
        await message.delete()
    except Exception:
        pass

    await message.reply_text(
        autoplay_text(new_state, mention),
        reply_markup=autoplay_markup(chat_id, new_state),
    )


# ── /autoplay on  /  /autoplay off  — explicit subcommand support ─────────────
@app.on_message(
    filters.command(["autoplayon", "aplon", "autoplayoff", "aploff"],
                    prefixes=["/", "!", ".", ","])
    & filters.group
    & ~BANNED_USERS
)
@AdminRightsCheck
async def autoplay_explicit(client, message: Message, _, chat_id):
    mention = message.from_user.mention
    cmd = message.command[0].lower()
    new_state = cmd in ("autoplayon", "aplon")
    await set_autoplay(chat_id, new_state)
    if new_state:
        await set_autoplay_owner(chat_id, message.from_user.id)

    try:
        await message.delete()
    except Exception:
        pass

    await message.reply_text(
        autoplay_text(new_state, mention),
        reply_markup=autoplay_markup(chat_id, new_state),
    )
