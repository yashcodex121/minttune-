import math
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ButtonStyle
import config
from SHUKLAMUSIC.utils.formatters import time_to_seconds


def track_markup(_, videoid, user_id, channel, fplay, chat_id=None):
    """Audio/Video pick card + Close."""
    return [
        [
            InlineKeyboardButton(
                text="🎵 𝑨𝒖𝒅𝒊𝒐",
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
                style=ButtonStyle.SUCCESS,
            ),
            InlineKeyboardButton(
                text="🎬 𝑽𝒊𝒅𝒆𝒐",
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
                style=ButtonStyle.PRIMARY,
            ),
        ],
        [
            InlineKeyboardButton(
                text="✖️ 𝑪𝒍𝒐𝒔𝒆",
                callback_data=f"forceclose {videoid}|{user_id}",
                style=ButtonStyle.DANGER,
            ),
        ],
    ]


def stream_markup_timer(_, chat_id, played, dur):
    """
    Exact screenshot layout:

    Row 1:  [  04:48 ────────── 5:13  ]   ← progress bar / timer
    Row 2:  [ ⏸ Pause ] [ ➕ ADD ME ] [ ⏭ ▶▶ ]
    Row 3:  [ 🔄 Autoplay  ON/OFF ]
    """
    played_sec   = time_to_seconds(played)
    duration_sec = time_to_seconds(dur)
    pct    = (played_sec / max(duration_sec, 1)) * 100
    filled = round((min(100, max(0, math.floor(pct))) / 100) * 10)
    # Unicode block progress bar
    bar    = "━" * filled + "─" * (10 - filled)
    cm, cs = divmod(played_sec, 60)
    tm, ts = divmod(duration_sec, 60)
    ct = f"{int(cm):02d}:{int(cs):02d}"
    tt = f"{int(tm):02d}:{int(ts):02d}"

    bot_username = getattr(config, "BOT_USERNAME", "").lstrip("@")

    return [
        # ── Progress bar row ──────────────────────────────────────────────
        [
            InlineKeyboardButton(
                text=f"{ct}  {bar}  {tt}",
                callback_data="GetTimer",
                style=ButtonStyle.PRIMARY,
            )
        ],
        # ── Main controls: Pause | ADD ME | Skip ──────────────────────────
        [
            InlineKeyboardButton(
                text="⏸ 𝑷𝒂𝒖𝒔𝒆",
                callback_data=f"ADMIN Pause|{chat_id}",
                style=ButtonStyle.PRIMARY,
            ),
            InlineKeyboardButton(
                text="➕ 𝑨𝑫𝑫 𝑴𝑬 ↗",
                url=f"https://t.me/{bot_username}?startgroup=true",
                style=ButtonStyle.SUCCESS,
            ),
            InlineKeyboardButton(
                text="⏭ ▶▶",
                callback_data=f"ADMIN Skip|{chat_id}",
                style=ButtonStyle.PRIMARY,
            ),
        ],
        # ── Autoplay toggle ───────────────────────────────────────────────
        [
            InlineKeyboardButton(
                text="🔄 𝑨𝒖𝒕𝒐𝒑𝒍𝒂𝒚",
                callback_data=f"ADMIN Autoplay|{chat_id}",
                style=ButtonStyle.SUCCESS,
            ),
        ],
    ]


def stream_markup(_, chat_id):
    """
    Static now-playing panel (before timer task):

    Row 1:  [ ⏸ Pause ] [ ➕ ADD ME ] [ ⏭ ▶▶ ]
    Row 2:  [ 🔄 Autoplay ]
    """
    bot_username = getattr(config, "BOT_USERNAME", "").lstrip("@")

    return [
        # ── Main controls ─────────────────────────────────────────────────
        [
            InlineKeyboardButton(
                text="⏸ 𝑷𝒂𝒖𝒔𝒆",
                callback_data=f"ADMIN Pause|{chat_id}",
                style=ButtonStyle.PRIMARY,
            ),
            InlineKeyboardButton(
                text="➕ 𝑨𝑫𝑫 𝑴𝑬 ↗",
                url=f"https://t.me/{bot_username}?startgroup=true",
                style=ButtonStyle.SUCCESS,
            ),
            InlineKeyboardButton(
                text="⏭ ▶▶",
                callback_data=f"ADMIN Skip|{chat_id}",
                style=ButtonStyle.PRIMARY,
            ),
        ],
        # ── Autoplay toggle ───────────────────────────────────────────────
        [
            InlineKeyboardButton(
                text="🔄 𝑨𝒖𝒕𝒐𝒑𝒍𝒂𝒚",
                callback_data=f"ADMIN Autoplay|{chat_id}",
                style=ButtonStyle.SUCCESS,
            ),
        ],
    ]


def playlist_markup(_, videoid, user_id, ptype, channel, fplay, chat_id=None):
    """Playlist: Audio / Video / Close."""
    return [
        [
            InlineKeyboardButton(
                text="🎵 𝑨𝒖𝒅𝒊𝒐",
                callback_data=f"SHUKLAPlaylists {videoid}|{user_id}|{ptype}|a|{channel}|{fplay}",
                style=ButtonStyle.SUCCESS,
            ),
            InlineKeyboardButton(
                text="🎬 𝑽𝒊𝒅𝒆𝒐",
                callback_data=f"SHUKLAPlaylists {videoid}|{user_id}|{ptype}|v|{channel}|{fplay}",
                style=ButtonStyle.PRIMARY,
            ),
        ],
        [
            InlineKeyboardButton(
                text="✖️ 𝑪𝒍𝒐𝒔𝒆",
                callback_data=f"forceclose {videoid}|{user_id}",
                style=ButtonStyle.DANGER,
            )
        ],
    ]


def livestream_markup(_, videoid, user_id, mode, channel, fplay):
    """Live stream card."""
    return [
        [
            InlineKeyboardButton(
                text="🔴 𝑳𝒊𝒗𝒆 𝑺𝒕𝒓𝒆𝒂𝒎",
                callback_data=f"MusicStream {videoid}|{user_id}|{mode}|{channel}|{fplay}",
                style=ButtonStyle.DANGER,
            )
        ],
        [
            InlineKeyboardButton(
                text="✖️ 𝑪𝒍𝒐𝒔𝒆",
                callback_data=f"forceclose {videoid}|{user_id}",
                style=ButtonStyle.DANGER,
            )
        ],
    ]


def slider_markup(_, videoid, user_id, query, query_type, channel, fplay):
    """Search result slider."""
    return [
        [
            InlineKeyboardButton(
                text="🎵 𝑨𝒖𝒅𝒊𝒐",
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
                style=ButtonStyle.SUCCESS,
            ),
            InlineKeyboardButton(
                text="🎬 𝑽𝒊𝒅𝒆𝒐",
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
                style=ButtonStyle.PRIMARY,
            ),
        ],
        [
            InlineKeyboardButton(
                text="◀️",
                callback_data=f"slider B|{query_type}|{query}|{user_id}|{channel}|{fplay}",
                style=ButtonStyle.PRIMARY,
            ),
            InlineKeyboardButton(
                text="✖️ 𝑪𝒍𝒐𝒔𝒆",
                callback_data=f"forceclose {videoid}|{user_id}",
                style=ButtonStyle.DANGER,
            ),
            InlineKeyboardButton(
                text="▶️",
                callback_data=f"slider F|{query_type}|{query}|{user_id}|{channel}|{fplay}",
                style=ButtonStyle.PRIMARY,
            ),
        ],
    ]
