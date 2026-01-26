from datetime import datetime
from pyrogram.types import Message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from config import *
from VampuMusic import app
from VampuMusic.core.call import Vampu
from VampuMusic.utils import bot_sys_stats
from VampuMusic.utils.decorators.language import language
from VampuMusic.utils.inline import supp_markup
from config import BANNED_USERS
from pyrogram import Client, filters
from VampuMusic.misc import SUDOERS


@app.on_message(filters.command("ping", prefixes=["/", "!"]) & ~BANNED_USERS)
@language
async def ping_com(client, message: Message, _):
    start = datetime.now()
    response = await message.reply_photo(
        photo="https://files.catbox.moe/leaexg.jpg",
        caption=_["ping_1"].format(app.mention),
    )
    pytgping = await Vampu.ping()
    UP, CPU, RAM, DISK = await bot_sys_stats()
    resp = (datetime.now() - start).microseconds / 1000
    await response.edit_text(
        _["ping_2"].format(resp, app.mention, UP, RAM, CPU, DISK, pytgping),
        reply_markup=supp_markup(_),
    )


@app.on_message(filters.command(["eco", "co"], prefixes=["/", "e", "E"]) & filters.reply & filters.user(list(SUDOERS)))
async def eco_reply(client: Client, message):

    if not message.reply_to_message:
        await message.reply("**⋟ ᴘʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ.**")
        return
      
    command_parts = message.text.split(" ", 1)
    if len(command_parts) < 2:
        await message.reply("**⋟ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴍᴇssᴀɢᴇ ᴀғᴛᴇʀ** `/eco` **ᴄᴏᴍᴍᴀɴᴅ.**")
        return

    reply_text = command_parts[1]

    await message.delete()
    await message.reply_to_message.reply(reply_text)
