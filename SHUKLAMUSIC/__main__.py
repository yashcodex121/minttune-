import asyncio
import importlib

try:
    import uvloop
    uvloop.install()
except ImportError:
    pass

# Create event loop BEFORE importing pyrogram
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall
import config
from SHUKLAMUSIC import LOGGER, app, userbot
from SHUKLAMUSIC.core.call import SHUKLA
from SHUKLAMUSIC.misc import sudo
from SHUKLAMUSIC.plugins import ALL_MODULES
from SHUKLAMUSIC.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS


async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("String Session Not Filled, Please Fill A Pyrogram Session")
        exit()
    await sudo()
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass
    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("SHUKLAMUSIC.plugins" + all_module)
    LOGGER("SHUKLAMUSIC.plugins").info("All Features Loaded...")
    await userbot.start()
    await SHUKLA.start()
    try:
        await SHUKLA.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("SHUKLAMUSIC").error("Please Start Your Log Group VoiceChat\n\nBot Stopping...")
        exit()
    except:
        pass
    await SHUKLA.decorators()
    LOGGER("SHUKLAMUSIC").info(
        "\n╔═════ஜ۩۞۩ஜ════╗\n  Bot Started Successfully\n╚═════ஜ۩۞۩ஜ════╝"
    )
    await idle()
    await app.stop()
    await userbot.stop()
    LOGGER("SHUKLAMUSIC").info("Bot Stopped.")


if __name__ == "__main__":
    loop.run_until_complete(init())