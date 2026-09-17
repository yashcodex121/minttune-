# -----------------------------------------------
# 🔸 StrangerMusic Project
# 🔹 Developed & Maintained by: Shashank Shukla (https://github.com/itzshukla)
# 📅 Copyright © 2022 – All Rights Reserved
# -----------------------------------------------
import random
from typing import Union
from pyrogram import filters, types
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram import enums
from SHUKLAMUSIC import app
from SHUKLAMUSIC.utils import help_pannel
from SHUKLAMUSIC.utils.database import get_lang
from SHUKLAMUSIC.utils.decorators.language import LanguageStart, languageCB
from SHUKLAMUSIC.utils.inline.help import help_back_markup, private_help_panel
from config import BANNED_USERS, SUPPORT_CHAT, SHASHANK_IMG
from strings import get_string, helpers
from SHUKLAMUSIC.utils.stuffs.buttons import BUTTONS
from SHUKLAMUSIC.utils.stuffs.helper import Helper

EFFECT_IDS = [
    5046509860389126442,
    5107584321108051014,
    5104841245755180586,
    5159385139981059251,
]

# ──────────────────────────────────────────────────────────────────────────────
# /help — PRIVATE (DM) handler  +  settings_back_helper callback
# ──────────────────────────────────────────────────────────────────────────────
@app.on_message(filters.command(["help"]) & filters.private & ~BANNED_USERS)
@app.on_callback_query(filters.regex("^settings_back_helper$") & ~BANNED_USERS)
async def helper_private(
    client, update: Union[types.Message, types.CallbackQuery]
):
    is_callback = isinstance(update, types.CallbackQuery)
    if is_callback:
        try:
            await update.answer()
        except Exception:
            pass
        chat_id = update.message.chat.id
        language = await get_lang(chat_id)
        _ = get_string(language)
        keyboard = help_pannel(_, True)
        try:
            await update.edit_message_text(
                _["help_1"].format(SUPPORT_CHAT), reply_markup=keyboard
            )
        except Exception:
            pass
    else:
        try:
            await update.delete()
        except Exception:
            pass
        language = await get_lang(update.chat.id)
        _ = get_string(language)
        keyboard = help_pannel(_)
        try:
            await update.reply_photo(
                random.choice(SHASHANK_IMG),
                caption=_["help_1"].format(SUPPORT_CHAT),
                reply_markup=keyboard,
                message_effect_id=random.choice(EFFECT_IDS),
            )
        except Exception:
            # Fallback if effect IDs are rejected (older clients)
            await update.reply_photo(
                random.choice(SHASHANK_IMG),
                caption=_["help_1"].format(SUPPORT_CHAT),
                reply_markup=keyboard,
            )


# ──────────────────────────────────────────────────────────────────────────────
# /help — GROUP handler
# ──────────────────────────────────────────────────────────────────────────────
@app.on_message(filters.command(["help"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def help_com_group(client, message: Message, _):
    keyboard = private_help_panel(_)
    try:
        await message.reply_text(
            _["help_2"],
            reply_markup=InlineKeyboardMarkup(keyboard),
            message_effect_id=random.choice(EFFECT_IDS),
        )
    except Exception:
        await message.reply_text(
            _["help_2"],
            reply_markup=InlineKeyboardMarkup(keyboard),
        )


# ──────────────────────────────────────────────────────────────────────────────
# help_callback — topic section navigation
# ──────────────────────────────────────────────────────────────────────────────
@app.on_callback_query(filters.regex("help_callback") & ~BANNED_USERS)
@languageCB
async def helper_cb(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    cb = callback_data.split(None, 1)[1]
    keyboard = help_back_markup(_)

    HELP_MAP = {
        "hb1":  helpers.HELP_1,  "hb2":  helpers.HELP_2,  "hb3":  helpers.HELP_3,
        "hb4":  helpers.HELP_4,  "hb5":  helpers.HELP_5,  "hb6":  helpers.HELP_6,
        "hb7":  helpers.HELP_7,  "hb8":  helpers.HELP_8,  "hb9":  helpers.HELP_9,
        "hb10": helpers.HELP_10, "hb11": helpers.HELP_11, "hb12": helpers.HELP_12,
        "hb13": helpers.HELP_13, "hb14": helpers.HELP_14, "hb15": helpers.HELP_15,
        "hb16": helpers.HELP_16, "hb17": helpers.HELP_17, "hb18": helpers.HELP_18,
        "hb19": helpers.HELP_19, "hb20": helpers.HELP_20, "hb21": helpers.HELP_21,
    }
    text = HELP_MAP.get(cb)
    if text:
        try:
            await CallbackQuery.edit_message_text(text, reply_markup=keyboard)
        except Exception:
            pass
    else:
        await CallbackQuery.answer("Section not found.", show_alert=True)


# ──────────────────────────────────────────────────────────────────────────────
# mbot_cb — bot management help page
# ──────────────────────────────────────────────────────────────────────────────
@app.on_callback_query(filters.regex("^mbot_cb$") & ~BANNED_USERS)
async def mbot_help_cb(client, CallbackQuery):
    try:
        await CallbackQuery.edit_message_text(
            Helper.HELP_M,
            reply_markup=InlineKeyboardMarkup(BUTTONS.MBUTTON),
        )
    except Exception:
        pass


# ──────────────────────────────────────────────────────────────────────────────
# managebot123 — FIXED: was missing `_` definition → NameError at runtime
# ──────────────────────────────────────────────────────────────────────────────
@app.on_callback_query(filters.regex("^managebot123") & ~BANNED_USERS)
async def on_back_button(client, CallbackQuery):
    try:
        await CallbackQuery.answer()
    except Exception:
        pass
    callback_data = CallbackQuery.data.strip()
    parts = callback_data.split(None, 1)
    cb = parts[1] if len(parts) > 1 else ""

    # Resolve language for this chat
    chat_id = CallbackQuery.message.chat.id
    language = await get_lang(chat_id)
    _ = get_string(language)          # ← was missing before — caused NameError

    keyboard = help_pannel(_, True)
    if cb == "settings_back_helper":
        try:
            await CallbackQuery.edit_message_text(
                _["help_1"].format(SUPPORT_CHAT), reply_markup=keyboard
            )
        except Exception:
            pass


# ──────────────────────────────────────────────────────────────────────────────
# mplus — dynamic plugin help pages
# ──────────────────────────────────────────────────────────────────────────────
@app.on_callback_query(filters.regex("^mplus") & ~BANNED_USERS)
async def mb_plugin_button(client, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    parts = callback_data.split(None, 1)
    cb = parts[1] if len(parts) > 1 else ""
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="mbot_cb")]]
    )
    if cb == "Okieeeeee":
        try:
            await CallbackQuery.edit_message_text(
                "`something errors`",
                reply_markup=keyboard,
                parse_mode=enums.ParseMode.MARKDOWN,
            )
        except Exception:
            pass
    else:
        try:
            text = getattr(Helper, cb, None)
            if text:
                await CallbackQuery.edit_message_text(text, reply_markup=keyboard)
            else:
                await CallbackQuery.answer("Page not found.", show_alert=True)
        except Exception:
            pass
