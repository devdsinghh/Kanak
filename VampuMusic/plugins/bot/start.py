import time
import random
import asyncio

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    InputMediaPhoto,
)

from py_yt import VideosSearch

import config
from VampuMusic import app
from VampuMusic.misc import _boot_
from VampuMusic.plugins.sudo.sudoers import sudoers_list
from VampuMusic.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    is_banned_user,
    is_on_off,
)
from VampuMusic.utils.decorators.language import LanguageStart
from VampuMusic.utils.formatters import get_readable_time
from VampuMusic.utils.inline import help_pannel, private_panel, start_panel
from strings import get_string
from config import BANNED_USERS


# ================= IMAGES ================= #

NEXIO = [
    "https://files.catbox.moe/ij3b0p.jpg",
    "https://files.catbox.moe/lna9eh.jpg",
    "https://files.catbox.moe/8i1ugj.jpg",
    "https://files.catbox.moe/raxhof.jpg",
    "https://files.catbox.moe/0z6diw.jpg",
    "https://files.catbox.moe/s8lc80.jpg",
    "https://files.catbox.moe/wyq373.jpg",
    "https://files.catbox.moe/7dwxl5.jpg",
    "https://files.catbox.moe/94v7qh.jpg",
    "https://files.catbox.moe/vxnw8u.jpg",
    "https://files.catbox.moe/ztzajy.jpg",
    "https://files.catbox.moe/kskt56.jpg",
]

# ================= STICKERS ================= #

Vampu_STKR = [
    "CAACAgUAAxkBAAIBO2i1Spi48ZdWCNehv-GklSI9aRYWAAJ9GAACXB-pVds_sm8brMEqHgQ",
    "CAACAgUAAxkBAAIBOmi1Sogwaoh01l5-e-lJkK1VNY6MAAIlGAACKI6wVVNEvN-6z3Z7HgQ",
    "CAACAgUAAxkBAAIBPGi1Spv1tlx90xM1Q7TRNyL0fhcJAAKDGgACZSupVbmJpWW9LmXJHgQ",
    "CAACAgUAAxkBAAIBPWi1SpxJZKxuWYsZ_G06j_G_9QGkAAIsHwACdd6xVd2HOWQPA_qtHgQ",
]

# ================= EFFECTS ================= #

EFFECT_IDS = [
    5046509860389126442,
    5107584321108051014,
    5104841245755180586,
    5159385139981059251,
]

emojis = ["🥰", "🔥", "💖", "😁", "😎", "🌚", "❤️‍🔥", "♥️", "🎉", "🙈"]

# ================= PRIVATE START ================= #

@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    await add_served_user(message.from_user.id)
    await message.react(random.choice(emojis))

    st = await message.reply_sticker(random.choice(Vampu_STKR))
    await asyncio.sleep(1)
    await st.delete()

    if len(message.text.split()) > 1:
        arg = message.text.split(None, 1)[1]

        # HELP
        if arg.startswith("help"):
            return await message.reply_photo(
                random.choice(NEXIO),
                caption=_["help_1"].format(config.SUPPORT_CHAT),
                reply_markup=help_pannel(_),
            )

        # SUDO LIST
        if arg.startswith("sud"):
            await sudoers_list(client, message, _)
            if await is_on_off(2):
                await app.send_message(
                    config.LOGGER_ID,
                    f"{message.from_user.mention} checked sudo list\nID: `{message.from_user.id}`",
                )
            return

        # TRACK INFO
        if arg.startswith("inf"):
            m = await message.reply_text("🔍 Searching...")
            query = arg.replace("info_", "", 1)
            results = VideosSearch(f"https://www.youtube.com/watch?v={query}", limit=1)

            for r in (await results.next())["result"]:
                title = r["title"]
                duration = r["duration"]
                views = r["viewCount"]["short"]
                thumb = r["thumbnails"][0]["url"].split("?")[0]
                link = r["link"]
                channel = r["channel"]["name"]
                ch_link = r["channel"]["link"]
                published = r["publishedTime"]

            await m.delete()

            await app.send_photo(
                message.chat.id,
                photo=thumb,
                caption=_["start_6"].format(
                    title, duration, views, published, ch_link, channel, app.mention
                ),
                message_effect_id=random.choice(EFFECT_IDS),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(_["S_B_8"], url=link),
                            InlineKeyboardButton(_["S_B_9"], url=config.SUPPORT_CHAT),
                        ]
                    ]
                ),
            )
            return

    # NORMAL START
    out = private_panel(_)
    await message.reply_photo(
        random.choice(NEXIO),
        caption=_["start_2"].format(message.from_user.mention, app.mention),
        message_effect_id=random.choice(EFFECT_IDS),
        reply_markup=InlineKeyboardMarkup(out),
    )


# ================= GROUP START ================= #

@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    uptime = int(time.time() - _boot_)
    await message.reply_photo(
        random.choice(NEXIO),
        caption=_["start_1"].format(app.mention, get_readable_time(uptime)),
        reply_markup=InlineKeyboardMarkup(start_panel(_)),
    )
    await add_served_chat(message.chat.id)


# ================= WELCOME ================= #

@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        try:
            lang = await get_lang(message.chat.id)
            _ = get_string(lang)

            if await is_banned_user(member.id):
                await message.chat.ban_member(member.id)
                return

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
                        )
                    )
                    return await app.leave_chat(message.chat.id)

                await message.reply_photo(
                    random.choice(NEXIO),
                    caption=_["start_3"].format(
                        message.from_user.mention,
                        app.mention,
                        message.chat.title,
                        app.mention,
                    ),
                    reply_markup=InlineKeyboardMarkup(start_panel(_)),
                )
                await add_served_chat(message.chat.id)
                await message.stop_propagation()

        except Exception as e:
            print(e)
