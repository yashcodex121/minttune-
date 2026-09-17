import asyncio

# Must set event loop BEFORE pyrogram import (Python 3.10 + uvloop fix)
_loop = asyncio.new_event_loop()
asyncio.set_event_loop(_loop)

from SHUKLAMUSIC.core.bot import SHUKLA
from SHUKLAMUSIC.core.dir import dirr
from SHUKLAMUSIC.core.git import git
from SHUKLAMUSIC.core.userbot import Userbot
from SHUKLAMUSIC.misc import dbb, heroku
from .logging import LOGGER

dirr()
git()
dbb()
heroku()

app = SHUKLA()
userbot = Userbot()

from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()

APP = "InflexOwnerBot"