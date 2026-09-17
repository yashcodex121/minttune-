from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ButtonStyle
from config import SUPPORT_CHAT

def botplaylist_markup(_):
    return [
        [
            InlineKeyboardButton(text="💬 𝑺𝒖𝒑𝒑𝒐𝒓𝒕", url=SUPPORT_CHAT, style=ButtonStyle.PRIMARY),
            InlineKeyboardButton(text="✖️ 𝑪𝒍𝒐𝒔𝒆", callback_data="close", style=ButtonStyle.DANGER),
        ],
    ]

def close_markup(_):
    return InlineKeyboardMarkup([[
        InlineKeyboardButton(text="✖️ 𝑪𝒍𝒐𝒔𝒆", callback_data="close", style=ButtonStyle.DANGER),
    ]])

def supp_markup(_):
    return InlineKeyboardMarkup([[
        InlineKeyboardButton(text="💬 𝑺𝒖𝒑𝒑𝒐𝒓𝒕", url=SUPPORT_CHAT, style=ButtonStyle.PRIMARY),
    ]])