from typing import Union
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ButtonStyle

def setting_markup(_):
    return [
        [
            InlineKeyboardButton(text="👥 𝑨𝒖𝒕𝒉 𝑼𝒔𝒆𝒓𝒔", callback_data="AU", style=ButtonStyle.PRIMARY),
            InlineKeyboardButton(text="🌐 𝑳𝒂𝒏𝒈𝒖𝒂𝒈𝒆", callback_data="LG", style=ButtonStyle.SUCCESS),
        ],
        [InlineKeyboardButton(text="🎵 𝑷𝒍𝒂𝒚 𝑴𝒐𝒅𝒆", callback_data="PM", style=ButtonStyle.PRIMARY)],
        [InlineKeyboardButton(text="🗳️ 𝑽𝒐𝒕𝒆 𝑴𝒐𝒅𝒆", callback_data="VM", style=ButtonStyle.SUCCESS)],
        [InlineKeyboardButton(text="✖️ 𝑪𝒍𝒐𝒔𝒆", callback_data="close", style=ButtonStyle.DANGER)],
    ]

def vote_mode_markup(_, current, mode: Union[bool, str] = None):
    return [
        [
            InlineKeyboardButton(text="🗳️ 𝑽𝒐𝒕𝒊𝒏𝒈 𝑴𝒐𝒅𝒆 ➜", callback_data="VOTEANSWER", style=ButtonStyle.PRIMARY),
            InlineKeyboardButton(
                text="✅ 𝑶𝒏" if mode == True else "❌ 𝑶𝒇𝒇",
                callback_data="VOMODECHANGE",
                style=ButtonStyle.SUCCESS if mode == True else ButtonStyle.DANGER,
            ),
        ],
        [
            InlineKeyboardButton(text="➖𝟐", callback_data="FERRARIUDTI M", style=ButtonStyle.DANGER),
            InlineKeyboardButton(text=f"𝑪𝒖𝒓𝒓𝒆𝒏𝒕: {current}", callback_data="ANSWERVOMODE", style=ButtonStyle.PRIMARY),
            InlineKeyboardButton(text="➕𝟐", callback_data="FERRARIUDTI A", style=ButtonStyle.SUCCESS),
        ],
        [
            InlineKeyboardButton(text="◀️ 𝑩𝒂𝒄𝒌", callback_data="settings_helper", style=ButtonStyle.PRIMARY),
            InlineKeyboardButton(text="✖️ 𝑪𝒍𝒐𝒔𝒆", callback_data="close", style=ButtonStyle.DANGER),
        ],
    ]

def auth_users_markup(_, status: Union[bool, str] = None):
    return [
        [InlineKeyboardButton(
            text="✅ 𝑬𝒏𝒂𝒃𝒍𝒆𝒅" if status else "❌ 𝑫𝒊𝒔𝒂𝒃𝒍𝒆𝒅",
            callback_data="AUTHANSWER",
            style=ButtonStyle.SUCCESS if status else ButtonStyle.DANGER,
        )],
        [
            InlineKeyboardButton(text="◀️ 𝑩𝒂𝒄𝒌", callback_data="settings_helper", style=ButtonStyle.PRIMARY),
            InlineKeyboardButton(text="✖️ 𝑪𝒍𝒐𝒔𝒆", callback_data="close", style=ButtonStyle.DANGER),
        ],
    ]

def playmode_users_markup(_, status: Union[bool, str] = None):
    return [
        [InlineKeyboardButton(
            text="🎯 𝑫𝒊𝒓𝒆𝒄𝒕" if status == "Direct" else "🔍 𝑰𝒏𝒍𝒊𝒏𝒆",
            callback_data="PLAYMODECHANGE",
            style=ButtonStyle.SUCCESS,
        )],
        [
            InlineKeyboardButton(text="◀️ 𝑩𝒂𝒄𝒌", callback_data="settings_helper", style=ButtonStyle.PRIMARY),
            InlineKeyboardButton(text="✖️ 𝑪𝒍𝒐𝒔𝒆", callback_data="close", style=ButtonStyle.DANGER),
        ],
    ]