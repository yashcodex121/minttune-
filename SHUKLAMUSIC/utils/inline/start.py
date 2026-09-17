from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ButtonStyle
import config
from SHUKLAMUSIC import app

def _clean_username(u): return u.lstrip("@")

def start_panel(_):
    return [
        [
            InlineKeyboardButton(text=_["S_B_1"], url=f"https://t.me/{app.username}?startgroup=true", style=ButtonStyle.PRIMARY),
            InlineKeyboardButton(text=_["S_B_2"], url=config.SUPPORT_CHAT, style=ButtonStyle.DANGER),
        ],
        [InlineKeyboardButton(text=_["S_B_4"], url=f"https://t.me/{app.username}?start=help", style=ButtonStyle.SUCCESS)],
    ]

def private_panel(_):
    return [
        [InlineKeyboardButton(text=_["S_B_3"], url=f"https://t.me/{app.username}?startgroup=true", style=ButtonStyle.PRIMARY)],
        [
            InlineKeyboardButton(text=_["S_B_5"], url=f"https://t.me/{_clean_username(config.OWNER_USERNAME)}", style=ButtonStyle.DANGER),
            InlineKeyboardButton(text=_["S_B_7"], url=config.SUPPORT_CHANNEL, style=ButtonStyle.SUCCESS),
        ],
        [
            InlineKeyboardButton(text=_["S_B_2"], url=config.SUPPORT_CHAT, style=ButtonStyle.DANGER),
            InlineKeyboardButton(text=_["S_B_6"], url=config.SUPPORT_CHANNEL, style=ButtonStyle.SUCCESS),
        ],
        [InlineKeyboardButton(text=_["S_B_4"], callback_data="settings_back_helper", style=ButtonStyle.SUCCESS)],
    ]