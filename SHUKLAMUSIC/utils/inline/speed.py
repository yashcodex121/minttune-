from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ButtonStyle

def speed_markup(_, chat_id):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(text="🕒 𝟎.𝟓𝐱", callback_data=f"SpeedUP {chat_id}|0.5", style=ButtonStyle.PRIMARY),
            InlineKeyboardButton(text="🕓 𝟎.𝟕𝟓𝐱", callback_data=f"SpeedUP {chat_id}|0.75", style=ButtonStyle.PRIMARY),
        ],
        [InlineKeyboardButton(text="✅ 𝟏.𝟎𝐱 𝑵𝒐𝒓𝒎𝒂𝒍", callback_data=f"SpeedUP {chat_id}|1.0", style=ButtonStyle.SUCCESS)],
        [
            InlineKeyboardButton(text="🕤 𝟏.𝟓𝐱", callback_data=f"SpeedUP {chat_id}|1.5", style=ButtonStyle.DANGER),
            InlineKeyboardButton(text="🕛 𝟐.𝟎𝐱", callback_data=f"SpeedUP {chat_id}|2.0", style=ButtonStyle.DANGER),
        ],
        [InlineKeyboardButton(text="✖️ 𝑪𝒍𝒐𝒔𝒆", callback_data="close", style=ButtonStyle.DANGER)],
    ])