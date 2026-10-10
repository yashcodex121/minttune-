import asyncio
import random
import time
import yt_dlp

from pyrogram import filters, enums
from pyrogram.enums import ChatType
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    Message,
)

import config
from SHUKLAMUSIC import app
from SHUKLAMUSIC.misc import _boot_
from SHUKLAMUSIC.plugins.sudo.sudoers import sudoers_list
from SHUKLAMUSIC.utils import bot_sys_stats
from SHUKLAMUSIC.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    get_served_chats,
    get_served_users,
    is_banned_user,
    is_on_off,
)

# Database import with fallback
try:
    from SHUKLAMUSIC.core.mongo import mongodb as db
except ImportError:
    try:
        from SHUKLAMUSIC.utils.database import mongodb as db
    except ImportError:
        db = None

from SHUKLAMUSIC.utils.decorators.language import LanguageStart
from SHUKLAMUSIC.utils.formatters import get_readable_time
from SHUKLAMUSIC.utils.inline import help_pannel, private_panel, start_panel
from config import BANNED_USERS
from strings import get_string

# ── Welcome DB (only if mongo is available) ──────────────────────────────────
welcome_db = db.welcome_config if db is not None else None

# ── Start images pool ─────────────────────────────────────────────────────────
YUMI_PICS = [
    "https://files.catbox.moe/qv2ob4.jpg",
    "https://files.catbox.moe/g7ul2x.jpg",
    "https://files.catbox.moe/6tc46s.jpg",
]

GREET = ["💞", "🥂", "🔍", "🧪", "⚡️", "🔥"]


# ── Helpers ───────────────────────────────────────────────────────────────────
async def delete_after(message, delay: int = 5):
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except Exception:
        pass


async def get_welcome_caption(msg_type, default_text, user, bot, chat=None):
    """Return custom DB caption if set, else default."""
    if welcome_db is None:
        return default_text
    try:
        data = await welcome_db.find_one({"_id": msg_type})
        if data and "message" in data:
            text = data["message"]
            text = text.replace("{name}", user.first_name or "")
            text = text.replace("{mention}", user.mention or "")
            text = text.replace(
                "{username}",
                f"@{user.username}" if user.username else "No Username",
            )
            text = text.replace("{bot_name}", bot.first_name or "")
            if chat:
                text = text.replace("{chat_name}", chat.title or "")
            return text
    except Exception:
        pass
    return default_text


# ── /setwelcome & /resetwelcome (owner only via config) ───────────────────────
@app.on_message(
    filters.command(["setwelcome_dm", "setwelcome_grp"])
    & filters.user(config.OWNER_ID)
)
async def set_welcome_msg(client, message: Message):
    cmd = message.command[0].lower()
    msg_type = "welcome_dm" if "dm" in cmd else "welcome_group"

    if len(message.command) < 2 and not message.reply_to_message:
        await message.reply_text(
            f"❌ <b>Usage:</b>\n<code>/{cmd} [Your HTML Message]</code>\n\n"
            "<b>Variables:</b>\n"
            "<code>{name}</code> - First Name\n"
            "<code>{mention}</code> - User Link\n"
            "<code>{username}</code> - @Username\n"
            "<code>{bot_name}</code> - Bot Name\n"
            "<code>{chat_name}</code> - Chat Name (Group only)"
        )
        return

    try:
        if message.reply_to_message:
            new_msg = (
                message.reply_to_message.text.html
                or message.reply_to_message.caption.html
            )
        else:
            new_msg = message.text.html.split(None, 1)[1]
    except (IndexError, AttributeError):
        return await message.reply_text(
            "❌ Text extract nahi kar paya. Dobara try karein."
        )

    if welcome_db is not None:
        await welcome_db.update_one(
            {"_id": msg_type},
            {"$set": {"message": new_msg}},
            upsert=True,
        )
    await message.reply_text(
        f"✅ <b>{msg_type.replace('_', ' ').upper()} message has been set!</b>"
    )


@app.on_message(
    filters.command(["resetwelcome"]) & filters.user(config.OWNER_ID)
)
async def reset_welcome_msg(client, message: Message):
    cmd_args = message.command
    msg_type = "welcome_dm"
    if len(cmd_args) > 1 and cmd_args[1].lower() in ("grp", "group"):
        msg_type = "welcome_group"

    if welcome_db is None:
        return await message.reply_text("ℹ️ Database not connected.")

    result = await welcome_db.delete_one({"_id": msg_type})
    if result.deleted_count:
        await message.reply_text(
            f"✅ <b>{msg_type.replace('_', ' ').upper()} reset!</b>\n"
            "<i>Bot will now use the default start message.</i>"
        )
    else:
        await message.reply_text(
            f"ℹ️ <b>No custom {msg_type.replace('_', ' ')} was saved.</b>"
        )


# ── /start — PRIVATE (DM) ─────────────────────────────────────────────────────
@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):

    # Reaction
    try:
        await message.react(emoji="😘")
    except Exception:
        pass

    # Premium sticker (auto-delete after 5 s)
    try:
        sticker_msg = await message.reply_sticker(
            "CAACAgIAAxkBAAIBm2d7F2v2AAHKRcqDAAGtKL9G8K5CpwACGCEAAnmTaEgLJfcv_g2AVAAE"
        )
        asyncio.create_task(delete_after(sticker_msg, 5))
    except Exception:
        pass

    # Quick loading animation
    loading = await message.reply_text(random.choice(GREET))
    await add_served_user(message.from_user.id)
    await asyncio.sleep(0.15)
    await loading.edit_text("<b>ᴅɪηɢ ᴅᴏηɢ...❤️‍🔥</b>")
    await asyncio.sleep(0.15)
    await loading.edit_text("<b>ᴅᴏᴏᴍ ᴍᴜsɪᴄ ♪</b>")
    await asyncio.sleep(0.15)
    await loading.edit_text("<b>sᴛᴧʀᴛed!🥀</b>")
    await asyncio.sleep(0.15)
    await loading.delete()

    # Deep-link handling
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]

        if name.startswith("help"):
            keyboard = help_pannel(_)
            await message.reply_photo(
                random.choice(YUMI_PICS),
                caption=_["help_1"],
                reply_markup=keyboard,
            )
            return

        elif name.startswith("sud"):
            await sudoers_list(client=client, message=message, _=_)
            return

        elif name.startswith("inf"):
            m = await message.reply_text("🔎")
            query = name.replace("info_", "", 1)
            video_url = f"https://www.youtube.com/watch?v={query}"

            def _fetch_yt_info():
                opts = {
                    "quiet": True,
                    "no_warnings": True,
                    "skip_download": True,
                    "noplaylist": True,
                }
                with yt_dlp.YoutubeDL(opts) as ydl:
                    return ydl.extract_info(video_url, download=False) or {}

            loop = asyncio.get_event_loop()
            info = await loop.run_in_executor(None, _fetch_yt_info)

            title = info.get("title") or "Unknown"
            dur_sec = int(info.get("duration") or 0)
            hh, rem = divmod(dur_sec, 3600)
            mm, ss = divmod(rem, 60)
            duration = f"{hh}:{mm:02d}:{ss:02d}" if hh else f"{mm}:{ss:02d}"

            vc = int(info.get("view_count") or 0)
            if vc >= 1_000_000_000:
                views = f"{vc / 1_000_000_000:.1f}B views"
            elif vc >= 1_000_000:
                views = f"{vc / 1_000_000:.1f}M views"
            elif vc >= 1_000:
                views = f"{vc / 1_000:.1f}K views"
            else:
                views = f"{vc} views" if vc else "Unknown Views"

            thumbnail = info.get("thumbnail") or ""
            channellink = (
                info.get("channel_url") or info.get("uploader_url") or ""
            )
            channel = info.get("uploader") or info.get("channel") or "Unknown"
            ud = info.get("upload_date") or ""
            if len(ud) == 8:
                months = [
                    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
                    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
                ]
                published = f"{ud[6:]} {months[int(ud[4:6]) - 1]} {ud[:4]}"
            else:
                published = ud or "Unknown"

            searched_text = _["start_6"].format(
                title, duration, views, published, channellink, channel, app.mention
            )
            key = InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton(text=_["S_B_8"], url=video_url),
                    InlineKeyboardButton(text=_["S_B_9"], url=config.SUPPORT_CHAT),
                ]]
            )
            await m.delete()
            await app.send_video(
                chat_id=message.chat.id,
                video=thumbnail,
                caption=searched_text,
                reply_markup=key,
            )
            return

    # ── Default DM start ──────────────────────────────────────────────────────
    served_chats = len(await get_served_chats())
    served_users = len(await get_served_users())
    UP, CPU, RAM, DISK = await bot_sys_stats()

    me = await client.get_me()
    bot_display_name = me.first_name or config.BOT_NAME or "Music Bot"

    default_caption = (
        f"Hey <b>{message.from_user.first_name}</b>✍️,\n\n"
        f"This is ˋ<b>{bot_display_name}</b>˴ ♩ [ <b>No Ads</b> ] ♩. "
        f"A music player bot with some awesome and useful features. "
        f"Click on the help button for more info.\n\n"
        f"<i>Use the buttons below to go inside or back.</i>"
    )

    final_caption = await get_welcome_caption(
        "welcome_dm",
        default_caption,
        message.from_user,
        me,
    )

    out = private_panel(_)
    user_first = message.from_user.first_name

    caption = (
        f"Hey <b>{user_first}</b>✍️,\n\n"
        f"╔══════════════════════════╗\n"
        f"║                                              ║\n"
        f"║  This is ˋ<b>{bot_display_name}</b>˴ ♩\n"
        f"║  <b>[ No Ads ] ♩</b>\n"
        f"║                                              ║\n"
        f"║  A music player bot with\n"
        f"║  some awesome and useful\n"
        f"║  features. Click on the\n"
        f"║  help button for more info.\n"
        f"║                                              ║\n"
        f"╚══════════════════════════╝\n\n"
        f"<i>Use the buttons below to go inside or back.</i>"
    )

    await app.send_photo(
        chat_id=message.from_user.id,
        photo=random.choice(YUMI_PICS),
        caption=caption,
        parse_mode=enums.ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(out),
    )

    if await is_on_off(2):
        try:
            await app.send_message(
                chat_id=config.LOGGER_ID,
                text=(
                    f"❖ {message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ.\n\n"
                    f"<b>๏ ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n"
                    f"<b>๏ ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}"
                ),
            )
        except Exception:
            pass


# ── /start — GROUP ─────────────────────────────────────────────────────────────
@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    try:
        await message.react(emoji="😘")
    except Exception:
        pass

    out = start_panel(_)
    uptime = int(time.time() - _boot_)

    default_caption = _["start_1"].format(app.mention, get_readable_time(uptime))
    me = await client.get_me()
    final_caption = await get_welcome_caption(
        "welcome_group",
        default_caption,
        message.from_user,
        me,
        message.chat,
    )

    await message.reply_photo(
        random.choice(YUMI_PICS),
        caption=final_caption,
        reply_markup=InlineKeyboardMarkup(out),
    )
    return await add_served_chat(message.chat.id)


# ── New member welcome ─────────────────────────────────────────────────────────
@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)

            if await is_banned_user(member.id):
                try:
                    await message.chat.ban_member(member.id)
                except Exception:
                    pass

            if member.id == app.id:
                if message.chat.type != ChatType.SUPERGROUP:
                    await message.reply_text(_["start_4"])
                    return await app.leave_chat(message.chat.id)

                if message.chat.id in await blacklisted_chats():
                    await message.reply_text(
                        _["start_5"].format(
                            app.mention,
                            f"https://t.me/{app.username}?start=sudolist",
                            config.SUPPORT_CHAT,
                        ),
                        disable_web_page_preview=True,
                    )
                    return await app.leave_chat(message.chat.id)

                out = start_panel(_)
                default_caption = _["start_3"].format(
                    message.from_user.mention,
                    app.mention,
                    message.chat.title,
                    app.mention,
                )
                me = await client.get_me()
                final_caption = await get_welcome_caption(
                    "welcome_group",
                    default_caption,
                    member,
                    me,
                    message.chat,
                )

                await message.reply_photo(
                    random.choice(YUMI_PICS),
                    has_spoiler=True,
                    caption=final_caption,
                    reply_markup=InlineKeyboardMarkup(out),
                )
                await add_served_chat(message.chat.id)
                await message.stop_propagation()

        except Exception as ex:
            print(ex)


# ── Language panel callback ────────────────────────────────────────────────────
@app.on_callback_query(filters.regex("^open_language_panel$") & ~BANNED_USERS)
async def open_language_panel(client, callback):
    """Opens the language selection panel from the start menu Language button."""
    from SHUKLAMUSIC.utils.database import get_lang
    from strings import languages_present
    language = await get_lang(callback.message.chat.id)
    _ = get_string(language)

    buttons = []
    row = []
    for lang_code, lang_name in languages_present.items():
        row.append(InlineKeyboardButton(
            text=f"{'✅ ' if lang_code == language else ''}{lang_name}",
            callback_data=f"setlang_{lang_code}",
        ))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([InlineKeyboardButton(
        text=_["BACK_BUTTON"],
        callback_data="settings_back_helper",
    )])

    try:
        await callback.answer()
        await callback.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception:
        pass


@app.on_callback_query(filters.regex(r"^setlang_(\w+)$") & ~BANNED_USERS)
async def set_lang_from_start(client, callback):
    """Sets language from the start menu Language panel."""
    from SHUKLAMUSIC.utils.database import get_lang, set_lang
    lang_code = callback.data.split("_", 1)[1]
    chat_id = callback.message.chat.id
    current = await get_lang(chat_id)

    if lang_code == current:
        return await callback.answer(_["lang_4"] if False else "Already set!", show_alert=False)

    from strings import languages
    if lang_code not in languages:
        return await callback.answer("Language not found.", show_alert=True)

    await set_lang(chat_id, lang_code)
    _ = get_string(lang_code)
    await callback.answer(_["lang_2"], show_alert=False)

    # Refresh buttons to show new tick
    from strings import languages_present
    buttons = []
    row = []
    for lc, ln in languages_present.items():
        row.append(InlineKeyboardButton(
            text=f"{'✅ ' if lc == lang_code else ''}{ln}",
            callback_data=f"setlang_{lc}",
        ))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([InlineKeyboardButton(
        text=_["BACK_BUTTON"],
        callback_data="settings_back_helper",
    )])

    try:
        await callback.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception:
        pass
