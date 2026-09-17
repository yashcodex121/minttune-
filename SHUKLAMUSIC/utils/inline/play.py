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
    Animated now-playing panel — screenshot style:

    Row 1:  [played_time ─────●───── total_time]   (progress slider feel)
    Row 2:  [⏸ Pause]  [🔄 Autoplay]  [⏭ Skip ▶▶]
    Row 3:  [🔁 Replay]  [🔀 Shuffle]  [🔂 Loop]
    Row 4:  [⏹ Stop / End]
    """
    played_sec   = time_to_seconds(played)
    duration_sec = time_to_seconds(dur)
    pct    = (played_sec / max(duration_sec, 1)) * 100
    filled = round((min(100, max(0, math.floor(pct))) / 100) * 10)
    bar    = "▰" * filled + "▱" * (10 - filled)
    cm, cs = divmod(played_sec, 60)
    tm, ts = divmod(duration_sec, 60)
    ct = f"{int(cm):02d}:{int(cs):02d}"
    tt = f"{int(tm):02d}:{int(ts):02d}"

    return [
        # ── Progress bar (slider style) ───────────────────────────────────
        [
            InlineKeyboardButton(
                text=f"{ct}  {bar}  {tt}",
                callback_data="GetTimer",
                style=ButtonStyle.PRIMARY,
            )
        ],
        # ── Main controls: Pause | Autoplay | Skip ────────────────────────
        [
            InlineKeyboardButton(
                text="⏸",
                callback_data=f"ADMIN Pause|{chat_id}",
                style=ButtonStyle.PRIMARY,
            ),
            InlineKeyboardButton(
                text="🔄 𝑨𝒖𝒕𝒐",
                callback_data=f"ADMIN Autoplay|{chat_id}",
                style=ButtonStyle.SUCCESS,
            ),
            InlineKeyboardButton(
                text="⏭ ▶▶",
                callback_data=f"ADMIN Skip|{chat_id}",
                style=ButtonStyle.PRIMARY,
            ),
        ],
        # ── Secondary controls: Resume | Replay | Shuffle | Loop ──────────
        [
            InlineKeyboardButton(
                text="▶️",
                callback_data=f"ADMIN Resume|{chat_id}",
                style=ButtonStyle.SUCCESS,
            ),
            InlineKeyboardButton(
                text="🔁",
                callback_data=f"ADMIN Replay|{chat_id}",
                style=ButtonStyle.PRIMARY,
            ),
            InlineKeyboardButton(
                text="🔀",
                callback_data=f"ADMIN Shuffle|{chat_id}",
                style=ButtonStyle.PRIMARY,
            ),
            InlineKeyboardButton(
                text="🔂",
                callback_data=f"ADMIN Loop|{chat_id}",
                style=ButtonStyle.PRIMARY,
            ),
        ],
        # ── Stop ──────────────────────────────────────────────────────────
        [
            InlineKeyboardButton(
                text="⏹ 𝑺𝒕𝒐𝒑 / 𝑬𝒏𝒅",
                callback_data=f"ADMIN Stop|{chat_id}",
                style=ButtonStyle.DANGER,
            ),
        ],
    ]


def stream_markup(_, chat_id):
    """
    Static now-playing panel (before timer task kicks in) — same layout:

    Row 1:  [⏸ Pause]  [🔄 Autoplay]  [⏭ Skip ▶▶]
    Row 2:  [▶️ Resume]  [🔁 Replay]  [🔀 Shuffle]  [🔂 Loop]
    Row 3:  [⏹ Stop / End]
    """
    return [
        # ── Main controls ─────────────────────────────────────────────────
        [
            InlineKeyboardButton(
                text="⏸",
                callback_data=f"ADMIN Pause|{chat_id}",
                style=ButtonStyle.PRIMARY,
            ),
            InlineKeyboardButton(
                text="🔄 𝑨𝒖𝒕𝒐",
                callback_data=f"ADMIN Autoplay|{chat_id}",
                style=ButtonStyle.SUCCESS,
            ),
            InlineKeyboardButton(
                text="⏭ ▶▶",
                callback_data=f"ADMIN Skip|{chat_id}",
                style=ButtonStyle.PRIMARY,
            ),
        ],
        # ── Secondary controls ────────────────────────────────────────────
        [
            InlineKeyboardButton(
                text="▶️",
                callback_data=f"ADMIN Resume|{chat_id}",
                style=ButtonStyle.SUCCESS,
            ),
            InlineKeyboardButton(
                text="🔁",
                callback_data=f"ADMIN Replay|{chat_id}",
                style=ButtonStyle.PRIMARY,
            ),
            InlineKeyboardButton(
                text="🔀",
                callback_data=f"ADMIN Shuffle|{chat_id}",
                style=ButtonStyle.PRIMARY,
            ),
            InlineKeyboardButton(
                text="🔂",
                callback_data=f"ADMIN Loop|{chat_id}",
                style=ButtonStyle.PRIMARY,
            ),
        ],
        # ── Stop ──────────────────────────────────────────────────────────
        [
            InlineKeyboardButton(
                text="⏹ 𝑺𝒕𝒐𝒑 / 𝑬𝒏𝒅",
                callback_data=f"ADMIN Stop|{chat_id}",
                style=ButtonStyle.DANGER,
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
