from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ButtonStyle

def song_markup(_, vidid):
    return [
        [
            InlineKeyboardButton(text="🎵 𝑨𝒖𝒅𝒊𝒐", callback_data=f"song_helper audio|{vidid}", style=ButtonStyle.SUCCESS),
            InlineKeyboardButton(text="🎬 𝑽𝒊𝒅𝒆𝒐", callback_data=f"song_helper video|{vidid}", style=ButtonStyle.PRIMARY),
        ],
        [InlineKeyboardButton(text="✖️ 𝑪𝒍𝒐𝒔𝒆", callback_data="close", style=ButtonStyle.DANGER)],
    ]