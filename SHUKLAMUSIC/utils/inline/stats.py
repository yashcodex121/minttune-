from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ButtonStyle

def stats_buttons(_, status):
    not_sudo = [InlineKeyboardButton(text="📊 𝑻𝒐𝒑 𝑶𝒗𝒆𝒓𝒂𝒍𝒍", callback_data="TopOverall", style=ButtonStyle.PRIMARY)]
    sudo = [
        InlineKeyboardButton(text="🔧 𝑺𝒖𝒅𝒐 𝑺𝒕𝒂𝒕𝒔", callback_data="bot_stats_sudo", style=ButtonStyle.DANGER),
        InlineKeyboardButton(text="📊 𝑻𝒐𝒑 𝑶𝒗𝒆𝒓𝒂𝒍𝒍", callback_data="TopOverall", style=ButtonStyle.PRIMARY),
    ]
    return InlineKeyboardMarkup([
        sudo if status else not_sudo,
        [InlineKeyboardButton(text="✖️ 𝑪𝒍𝒐𝒔𝒆", callback_data="close", style=ButtonStyle.DANGER)],
    ])

def back_stats_buttons(_):
    return InlineKeyboardMarkup([[
        InlineKeyboardButton(text="◀️ 𝑩𝒂𝒄𝒌", callback_data="stats_back", style=ButtonStyle.PRIMARY),
        InlineKeyboardButton(text="✖️ 𝑪𝒍𝒐𝒔𝒆", callback_data="close", style=ButtonStyle.DANGER),
    ]])