# -----------------------------------------------
# 🔸 StrangerMusic Project — Mood / Focus / Study Player
# 🔹 Developed & Maintained by: Shashank Shukla
# -----------------------------------------------
import random
from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    Message,
)
from pyrogram.enums import ButtonStyle
from SHUKLAMUSIC import app, YouTube
from SHUKLAMUSIC.misc import db
from SHUKLAMUSIC.utils.database import get_lang, is_active_chat
from SHUKLAMUSIC.utils.inline.play import stream_markup
from SHUKLAMUSIC.utils.inline.queue import aq_markup
from SHUKLAMUSIC.utils.stream.queue import put_queue
from SHUKLAMUSIC.core.call import SHUKLA
from SHUKLAMUSIC.utils.exceptions import AssistantErr
from config import BANNED_USERS, SUPPORT_CHAT
from strings import get_string

# ──────────────────────────────────────────────
# MODE QUERIES
# ──────────────────────────────────────────────
MOOD_QUERIES = {
    "happy":      ["happy bollywood songs 2024", "upbeat hindi songs", "feel good hindi songs", "dance hindi songs hit", "khushi wale gaane"],
    "sad":        ["sad bollywood songs 2024", "dard bhari hindi songs", "heart broken hindi songs", "emotional hindi songs arijit", "rona wale gaane"],
    "romantic":   ["romantic bollywood songs 2024", "love hindi songs", "pyaar wale gaane", "best romantic hindi songs", "love songs arijit singh"],
    "party":      ["party songs bollywood 2024", "dance party hindi songs", "dj hindi songs", "item songs bollywood", "party night hindi hits"],
    "chill":      ["chill hindi songs", "lofi hindi songs", "relaxing hindi songs", "soft hindi songs evening", "lo-fi bollywood chill"],
    "devotional": ["bhajan 2024", "popular bhajans hindi", "ganesh bhajan", "shiv bhajan hit", "morning bhajan aarti"],
    "workout":    ["gym songs hindi", "workout motivation hindi songs", "high energy hindi songs", "running songs hindi", "pump up hindi hits"],
    "sleep":      ["lullaby hindi songs", "sone ke gaane", "peaceful hindi songs night", "soft instrumental hindi", "calm hindi songs sleep"],
    "focus":      ["deep focus music study", "concentration music no lyrics", "focus instrumental background", "productivity music flow state", "ambient focus beats study"],
    "study":      ["study music lofi beats", "lofi hip hop study chill", "calm piano study music", "brain power study music", "coffee shop study sounds"],
}

# ──────────────────────────────────────────────
# MODE DISPLAY LABELS (stylish italic bold Unicode)
# ──────────────────────────────────────────────
MODE_LABELS = {
    "happy":      "😄 𝑯𝒂𝒑𝒑𝒚 𝑴𝒐𝒅𝒆",
    "sad":        "😢 𝑺𝒂𝒅 𝑴𝒐𝒅𝒆",
    "romantic":   "❤️ 𝑹𝒐𝒎𝒂𝒏𝒕𝒊𝒄 𝑴𝒐𝒅𝒆",
    "party":      "🎉 𝑷𝒂𝒓𝒕𝒚 𝑴𝒐𝒅𝒆",
    "chill":      "😌 𝑪𝒉𝒊𝒍𝒍 𝑴𝒐𝒅𝒆",
    "devotional": "🙏 𝑫𝒆𝒗𝒐𝒕𝒊𝒐𝒏𝒂𝒍 𝑴𝒐𝒅𝒆",
    "workout":    "💪 𝑾𝒐𝒓𝒌𝒐𝒖𝒕 𝑴𝒐𝒅𝒆",
    "sleep":      "😴 𝑺𝒍𝒆𝒆𝒑 𝑴𝒐𝒅𝒆",
    "focus":      "🎯 𝑭𝒐𝒄𝒖𝒔 𝑴𝒐𝒅𝒆",
    "study":      "📚 𝑺𝒕𝒖𝒅𝒚 𝑴𝒐𝒅𝒆",
}

# Button styles per mood
MODE_STYLES = {
    "happy":      ButtonStyle.SUCCESS,
    "sad":        ButtonStyle.PRIMARY,
    "romantic":   ButtonStyle.DANGER,
    "party":      ButtonStyle.SUCCESS,
    "chill":      ButtonStyle.PRIMARY,
    "devotional": ButtonStyle.SUCCESS,
    "workout":    ButtonStyle.DANGER,
    "sleep":      ButtonStyle.PRIMARY,
    "focus":      ButtonStyle.PRIMARY,
    "study":      ButtonStyle.SUCCESS,
}


# ──────────────────────────────────────────────
# MOOD SELECTOR KEYBOARD
# ──────────────────────────────────────────────
def mood_buttons():
    moods = list(MODE_LABELS.items())
    rows = []
    for i in range(0, len(moods), 2):
        row = []
        for key, label in moods[i : i + 2]:
            row.append(
                InlineKeyboardButton(
                    label,
                    callback_data=f"mood_play {key}",
                    style=MODE_STYLES.get(key, ButtonStyle.PRIMARY),
                )
            )
        rows.append(row)
    # Bottom: End + Support
    rows.append(
        [
            InlineKeyboardButton(
                "⏹ 𝑬𝒏𝒅",
                callback_data="close",
                style=ButtonStyle.DANGER,
            ),
            InlineKeyboardButton(
                "💬 𝑺𝒖𝒑𝒑𝒐𝒓𝒕",
                url=SUPPORT_CHAT,
                style=ButtonStyle.PRIMARY,
            ),
        ]
    )
    return InlineKeyboardMarkup(rows)


def mood_now_playing_buttons(chat_id):
    """Inline buttons shown on the now-playing mood message (no thumbnail)."""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "⏹ 𝑬𝒏𝒅",
                    callback_data=f"ADMIN Stop|{chat_id}",
                    style=ButtonStyle.DANGER,
                ),
                InlineKeyboardButton(
                    "💬 𝑺𝒖𝒑𝒑𝒐𝒓𝒕",
                    url=SUPPORT_CHAT,
                    style=ButtonStyle.PRIMARY,
                ),
            ]
        ]
    )


def mood_queue_buttons(chat_id):
    """Inline buttons for queue-added mood message."""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "⏹ 𝑬𝒏𝒅",
                    callback_data=f"ADMIN Stop|{chat_id}",
                    style=ButtonStyle.DANGER,
                ),
                InlineKeyboardButton(
                    "💬 𝑺𝒖𝒑𝒑𝒐𝒓𝒕",
                    url=SUPPORT_CHAT,
                    style=ButtonStyle.PRIMARY,
                ),
            ]
        ]
    )


# ──────────────────────────────────────────────
# /mood COMMAND
# ──────────────────────────────────────────────
@app.on_message(
    filters.command(["mood"], prefixes=["/", "!", ".", ","]) & filters.group & ~BANNED_USERS
)
async def mood_command(client, message: Message):
    try:
        await message.delete()
    except Exception:
        pass
    await message.reply_text(
        "🎵 <b>𝑴𝒐𝒐𝒅 𝑺𝒆𝒍𝒆𝒄𝒕𝒐𝒓</b>\n\n"
        "𝑪𝒉𝒐𝒐𝒔𝒆 𝒚𝒐𝒖𝒓 𝒎𝒐𝒐𝒅\n\n\n"
        "🎶 <i>𝑰 𝒘𝒊𝒍𝒍 𝒑𝒊𝒄𝒌 𝒕𝒉𝒆 𝒑𝒆𝒓𝒇𝒆𝒄𝒕 𝒔𝒐𝒏𝒈 𝒋𝒖𝒔𝒕 𝒇𝒐𝒓 𝒚𝒐𝒖!</i>",
        reply_markup=mood_buttons(),
    )


# ──────────────────────────────────────────────
# MOOD CALLBACK — plays song WITHOUT thumbnail
# ──────────────────────────────────────────────
@app.on_callback_query(filters.regex(r"^mood_play (\w+)$") & ~BANNED_USERS)
async def mood_callback(client, callback: CallbackQuery):
    mood = callback.data.split()[1]
    user = callback.from_user.mention
    chat_id = callback.message.chat.id

    queries = MOOD_QUERIES.get(mood)
    if not queries:
        return await callback.answer("Unknown mood!", show_alert=True)

    mode_label = MODE_LABELS.get(mood, mood)

    await callback.answer(f"🎵 Finding {mode_label} song...")

    # Edit to searching state (text only, no photo)
    try:
        msg = await callback.message.edit_text(
            f"🔍 <b>{mode_label}</b>\n\n"
            f"╔══════════════════╗\n"
            f"║  𝑺𝒆𝒂𝒓𝒄𝒉𝒊𝒏𝒈...   ║\n"
            f"╚══════════════════╝\n\n"
            f"<i>🎵 𝑷𝒍𝒆𝒂𝒔𝒆 𝒘𝒂𝒊𝒕...</i>"
        )
    except Exception:
        msg = await callback.message.reply_text(
            f"🔍 <b>{mode_label}</b>\n\n"
            f"<i>🎵 𝑷𝒍𝒆𝒂𝒔𝒆 𝒘𝒂𝒊𝒕...</i>"
        )

    try:
        # ── Try up to 8 queries ──────────────────────────────────────────
        all_queries = queries * 2
        random.shuffle(all_queries)

        track_info = None   # ← renamed from 'details' to avoid any `_` confusion
        file_path  = None
        direct     = False
        tried_vids = set()

        for q in all_queries[:8]:
            try:
                # YouTube.track returns (track_dict, vidid_str)
                # We use a named variable 'vidid_str' so we NEVER shadow `_`
                result_pair = await YouTube.track(q)
                if not result_pair:
                    continue
                track_info_candidate, vidid_str = result_pair
                if not track_info_candidate:
                    continue
                if track_info_candidate.get("vidid") in tried_vids:
                    continue
                tried_vids.add(track_info_candidate["vidid"])

                # Duration check (max 30 min)
                dur_str = track_info_candidate.get("duration_min", "00:00")
                parts   = dur_str.split(":")
                total_sec = sum(int(x) * 60 ** i for i, x in enumerate(reversed(parts)))
                if total_sec > 1800 or total_sec < 30:
                    continue

                # Try downloading
                fp, dr = await YouTube.download(
                    track_info_candidate["vidid"],
                    msg,
                    videoid=True,
                    video=None,
                    title=track_info_candidate.get("title", ""),
                )
                if fp:
                    track_info = track_info_candidate
                    file_path  = fp
                    direct     = dr
                    break
            except Exception:
                continue

        if not track_info or not file_path:
            return await msg.edit_text(
                f"❌ <b>𝑪𝒐𝒖𝒍𝒅 𝒏𝒐𝒕 𝒇𝒊𝒏𝒅 𝒂 𝒔𝒐𝒏𝒈 𝒇𝒐𝒓 {mode_label}</b>\n\n"
                "<i>𝑻𝒓𝒚 𝒂𝒈𝒂𝒊𝒏 𝒐𝒓 𝒄𝒉𝒐𝒐𝒔𝒆 𝒂𝒏𝒐𝒕𝒉𝒆𝒓 𝒎𝒐𝒐𝒅 🎵</i>",
                reply_markup=mood_buttons(),
            )

        # ── Get language strings (safe: never overwrites `_`) ────────────
        language = await get_lang(chat_id)
        lang_str = get_string(language)  # ← stored as 'lang_str', not '_'

        song_title    = track_info["title"]
        song_duration = track_info["duration_min"]
        queue_file    = file_path if direct else f"vid_{track_info['vidid']}"

        if await is_active_chat(chat_id):
            # ── Add to queue ─────────────────────────────────────────────
            await put_queue(
                chat_id,
                chat_id,
                queue_file,
                song_title,
                song_duration,
                user,
                track_info["vidid"],
                callback.from_user.id,
                "audio",
            )
            position = len(db.get(chat_id, [])) - 1
            await msg.edit_text(
                f"✅ <b>𝑨𝒅𝒅𝒆𝒅 𝒕𝒐 𝑸𝒖𝒆𝒖𝒆 #{position}</b>\n\n"
                f"🎵 <b>𝑺𝒐𝒏𝒈 :</b> <code>{song_title[:40]}</code>\n"
                f"⏱ <b>𝑫𝒖𝒓 :</b> <code>{song_duration}</code>\n"
                f"🎭 <b>𝑴𝒐𝒅𝒆 :</b> {mode_label}\n"
                f"👤 <b>𝑩𝒚 :</b> {user}",
                reply_markup=mood_queue_buttons(chat_id),
            )
        else:
            # ── Start fresh playback ─────────────────────────────────────
            db[chat_id] = []
            try:
                await SHUKLA.join_call(chat_id, chat_id, file_path, video=None)
            except AssistantErr as e:
                return await msg.edit_text(str(e))

            await put_queue(
                chat_id,
                chat_id,
                queue_file,
                song_title,
                song_duration,
                user,
                track_info["vidid"],
                callback.from_user.id,
                "audio",
            )

            # ── Now-playing message: TEXT ONLY (no thumbnail) ────────────
            run = await app.send_message(
                chat_id,
                f"╔══════════════════════╗\n"
                f"║  🎵 <b>𝑵𝒐𝒘 𝑷𝒍𝒂𝒚𝒊𝒏𝒈</b>  ║\n"
                f"╚══════════════════════╝\n\n"
                f"🎶 <b>𝑺𝒐𝒏𝒈  :</b>  <code>{song_title[:40]}</code>\n"
                f"🎭 <b>𝑴𝒐𝒅𝒆  :</b>  {mode_label}\n"
                f"⏱ <b>𝑫𝒖𝒓   :</b>  <code>{song_duration}</code>\n"
                f"👤 <b>𝑹𝒆𝒒   :</b>  {user}",
                reply_markup=mood_now_playing_buttons(chat_id),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "stream"

            # Delete the searching message
            try:
                await msg.delete()
            except Exception:
                pass

    except Exception as e:
        try:
            await msg.edit_text(
                f"❌ <b>𝑬𝒓𝒓𝒐𝒓: {type(e).__name__}</b>\n\n"
                f"<i>𝑷𝒍𝒆𝒂𝒔𝒆 𝒕𝒓𝒚 𝒂𝒈𝒂𝒊𝒏 🎵</i>",
                reply_markup=mood_buttons(),
            )
        except Exception:
            pass
