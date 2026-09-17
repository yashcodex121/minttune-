import math
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ButtonStyle
import config
from SHUKLAMUSIC.utils.formatters import time_to_seconds


def track_markup(_, videoid, user_id, channel, fplay, chat_id=None):
    """Shown when a URL/search result is found — Audio/Video pick + Autoplay toggle + Close."""
    rows = [
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
    return rows


def stream_markup_timer(_, chat_id, played, dur):
    """Animated progress-bar markup shown on the now-playing message."""
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
        # ── Progress bar ──────────────────────────────────────────────────
        [
            InlineKeyboardButton(
                text=f"⏱ {ct} {bar} {tt}",
                callback_data="GetTimer",
                style=ButtonStyle.PRIMARY,
            )
        ],
        # ── Playback controls ─────────────────────────────────────────────
        [
            InlineKeyboardButton(text="▶️",  callback_data=f"ADMIN Resume|{chat_id}", style=ButtonStyle.SUCCESS),
            InlineKeyboardButton(text="⏭",   callback_data=f"ADMIN Skip|{chat_id}",   style=ButtonStyle.PRIMARY),
            InlineKeyboardButton(text="⏸",   callback_data=f"ADMIN Pause|{chat_id}",  style=ButtonStyle.PRIMARY),
            InlineKeyboardButton(text="⏹",   callback_data=f"ADMIN Stop|{chat_id}",   style=ButtonStyle.DANGER),
        ],
        # ── Queue controls ────────────────────────────────────────────────
        [
            InlineKeyboardButton(text="🔁 𝑹𝒆𝒑𝒍𝒂𝒚",   callback_data=f"ADMIN Replay|{chat_id}",   style=ButtonStyle.PRIMARY),
            InlineKeyboardButton(text="🔀 𝑺𝒉𝒖𝒇𝒇𝒍𝒆", callback_data=f"ADMIN Shuffle|{chat_id}", style=ButtonStyle.PRIMARY),
            InlineKeyboardButton(text="🔂 𝑳𝒐𝒐𝒑",     callback_data=f"ADMIN Loop|{chat_id}",     style=ButtonStyle.PRIMARY),
        ],
        # ── Autoplay (Spotify-style) ──────────────────────────────────────
        [
            InlineKeyboardButton(
                text="🔄 𝑨𝒖𝒕𝒐𝒑𝒍𝒂𝒚",
                callback_data=f"ADMIN Autoplay|{chat_id}",
                style=ButtonStyle.SUCCESS,
            )
        ],
        # ── Close ─────────────────────────────────────────────────────────
        [
            InlineKeyboardButton(
                text="✖️ 𝑪𝒍𝒐𝒔𝒆",
                callback_data="close",
                style=ButtonStyle.DANGER,
            )
        ],
    ]


def stream_markup(_, chat_id):
    """Static now-playing markup (before the timer task kicks in)."""
    return [
        # ── Playback controls ─────────────────────────────────────────────
        [
            InlineKeyboardButton(text="▶️",  callback_data=f"ADMIN Resume|{chat_id}", style=ButtonStyle.SUCCESS),
            InlineKeyboardButton(text="⏭",   callback_data=f"ADMIN Skip|{chat_id}",   style=ButtonStyle.PRIMARY),
            InlineKeyboardButton(text="⏸",   callback_data=f"ADMIN Pause|{chat_id}",  style=ButtonStyle.PRIMARY),
            InlineKeyboardButton(text="⏹",   callback_data=f"ADMIN Stop|{chat_id}",   style=ButtonStyle.DANGER),
        ],
        # ── Queue controls ────────────────────────────────────────────────
        [
            InlineKeyboardButton(text="🔁 𝑹𝒆𝒑𝒍𝒂𝒚",   callback_data=f"ADMIN Replay|{chat_id}",   style=ButtonStyle.PRIMARY),
            InlineKeyboardButton(text="🔀 𝑺𝒉𝒖𝒇𝒇𝒍𝒆", callback_data=f"ADMIN Shuffle|{chat_id}", style=ButtonStyle.PRIMARY),
            InlineKeyboardButton(text="🔂 𝑳𝒐𝒐𝒑",     callback_data=f"ADMIN Loop|{chat_id}",     style=ButtonStyle.PRIMARY),
        ],
        # ── Autoplay (Spotify-style) ──────────────────────────────────────
        [
            InlineKeyboardButton(
                text="🔄 𝑨𝒖𝒕𝒐𝒑𝒍𝒂𝒚",
                callback_data=f"ADMIN Autoplay|{chat_id}",
                style=ButtonStyle.SUCCESS,
            )
        ],
        # ── Close ─────────────────────────────────────────────────────────
        [
            InlineKeyboardButton(
                text="✖️ 𝑪𝒍𝒐𝒔𝒆",
                callback_data="close",
                style=ButtonStyle.DANGER,
            )
        ],
    ]


def playlist_markup(_, videoid, user_id, ptype, channel, fplay, chat_id=None):
    """Playlist selection: Audio / Video / Close."""
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
    """Live stream card: Stream + Close."""
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
    """Search result slider: Audio / Video / Prev / Close / Next."""
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
