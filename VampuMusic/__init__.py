from VampuMusic.core.bot import Vampu
from VampuMusic.core.dir import dirr
from VampuMusic.core.git import git
from VampuMusic.core.userbot import Userbot
from VampuMusic.misc import dbb, heroku
from .logging import LOGGER

dirr()
git()
dbb()
heroku()

app = Vampu()
userbot = Userbot()


from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()

