from typing import Union
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ButtonStyle
from SHUKLAMUSIC import app

def queue_markup(_, DURATION, CPLAY, videoid, played=None, dur=None):
    not_dur = [[
        InlineKeyboardButton(text="📋 𝑸𝒖𝒆𝒖𝒆", callback_data=f"GetQueued {CPLAY}|{videoid}", style=ButtonStyle.PRIMARY),
        InlineKeyboardButton(text="✖️ 𝑪𝒍𝒐𝒔𝒆", callback_data="close", style=ButtonStyle.DANGER),
    ]]
    with_dur = [
        [InlineKeyboardButton(text=_["QU_B_2"].format(played, dur), callback_data="GetTimer", style=ButtonStyle.PRIMARY)],
        [
            InlineKeyboardButton(text="▶️", callback_data=f"ADMIN Resume|{CPLAY}", style=ButtonStyle.SUCCESS),
            InlineKeyboardButton(text="⏸", callback_data=f"ADMIN Pause|{CPLAY}", style=ButtonStyle.PRIMARY),
            InlineKeyboardButton(text="⏭", callback_data=f"ADMIN Skip|{CPLAY}", style=ButtonStyle.SUCCESS),
            InlineKeyboardButton(text="⏹", callback_data=f"ADMIN Stop|{CPLAY}", style=ButtonStyle.DANGER),
        ],
        [
            InlineKeyboardButton(text="📋 𝑸𝒖𝒆𝒖𝒆", callback_data=f"GetQueued {CPLAY}|{videoid}", style=ButtonStyle.PRIMARY),
            InlineKeyboardButton(text="✖️ 𝑪𝒍𝒐𝒔𝒆", callback_data="close", style=ButtonStyle.DANGER),
        ],
    ]
    return InlineKeyboardMarkup(not_dur if DURATION == "Unknown" else with_dur)

def queue_back_markup(_, CPLAY):
    return InlineKeyboardMarkup([[
        InlineKeyboardButton(text="◀️ 𝑩𝒂𝒄𝒌", callback_data=f"queue_back_timer {CPLAY}", style=ButtonStyle.PRIMARY),
        InlineKeyboardButton(text="✖️ 𝑪𝒍𝒐𝒔𝒆", callback_data="close", style=ButtonStyle.DANGER),
    ]])

def aq_markup(_, chat_id):
    return [
        [InlineKeyboardButton(text="➕ 𝑨𝒅𝒅 𝑴𝒆", url=f"https://t.me/{app.username}?startgroup=true", style=ButtonStyle.PRIMARY)],
        [
            InlineKeyboardButton(text="▶️", callback_data=f"ADMIN Resume|{chat_id}", style=ButtonStyle.SUCCESS),
            InlineKeyboardButton(text="⏸", callback_data=f"ADMIN Pause|{chat_id}", style=ButtonStyle.PRIMARY),
            InlineKeyboardButton(text="⏭", callback_data=f"ADMIN Skip|{chat_id}", style=ButtonStyle.SUCCESS),
            InlineKeyboardButton(text="⏹", callback_data=f"ADMIN Stop|{chat_id}", style=ButtonStyle.DANGER),
        ],
        [InlineKeyboardButton(text="✖️ 𝑪𝒍𝒐𝒔𝒆", callback_data="close", style=ButtonStyle.DANGER)],
    ]