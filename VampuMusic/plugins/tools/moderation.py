from VampuMusic import app
from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from VampuMusic.utils.vampu_ban import admin_filter
from pyrogram.types import ChatPermissions
from pyrogram.errors import FloodWait
import asyncio


@app.on_message(filters.command("unbanall") & filters.group)
async def unban_all(_, msg):
    chat_id = msg.chat.id
    user_id = msg.from_user.id

    try:
        user = await app.get_chat_member(chat_id, user_id)
        user_permission = user.privileges.can_restrict_members if user.privileges else False

        if not user_permission:
            await msg.reply_text(
                "» ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴇ ʀɪɢʜᴛ ᴛᴏ ʀᴇsᴛʀɪᴄᴛ ᴜsᴇʀs.",
            )
            return

        me = await app.get_me()
        BOT_ID = me.id

        bot = await app.get_chat_member(chat_id, BOT_ID)
        bot_permission = bot.privileges.can_restrict_members if bot.privileges else False

        if not bot_permission:
            await msg.reply_text(
                "» ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴇ ʀɪɢʜᴛ ᴛᴏ ʀᴇsᴛʀɪᴄᴛ ᴜsᴇʀs.",
            )
            return

        user_mention = msg.from_user.mention if msg.from_user else "ʜɪᴅᴅᴇɴ ᴜsᴇʀ"
        status_msg = await msg.reply_text(f"» ᴜɴʙᴀɴᴀʟʟ sᴛᴀʀᴛᴇᴅ ʙʏ {user_mention}")

        banned_users = []
        async for m in app.get_chat_members(chat_id, filter=enums.ChatMembersFilter.BANNED):
            if m.user and hasattr(m.user, 'id'):
                banned_users.append(m.user.id)
            else:
                continue

        if not banned_users:
            await status_msg.delete()
            await msg.reply_text("» ɴᴏ ʙᴀɴɴᴇᴅ ᴜsᴇʀs ᴛᴏ ᴜɴʙᴀɴ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ.")
            return

        unbanned_count = 0
        for user_id in banned_users:
            try:
                await app.unban_chat_member(chat_id, user_id)
                unbanned_count += 1
            except Exception:
                pass

        await status_msg.delete()
        
        await msg.reply_text(
            f"» ᴜɴʙᴀɴɴᴇᴅ {unbanned_count} ᴜsᴇʀs ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ ✅",
        )

    except Exception as e:
        await msg.reply_text(
            f"» sᴏᴍᴇ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀᴇᴅ : {e}",
        )


@app.on_message(filters.command("unmuteall") & filters.group)
async def unmute_all(_, msg):
    chat_id = msg.chat.id
    user_id = msg.from_user.id
    
    user = await app.get_chat_member(chat_id, user_id)
    user_permission = user.privileges.can_restrict_members if user.privileges else False

    if not user_permission:
        return await msg.reply_text("» ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴜɴᴍᴜᴛᴇ ᴍᴇᴍʙᴇʀs.")
    
    me = await app.get_me()
    bot = await app.get_chat_member(chat_id, me.id)
    bot_permission = bot.privileges.can_restrict_members if bot.privileges else False
    
    if not bot_permission:
        return await msg.reply_text("» ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴜɴᴍᴜᴛᴇ ᴍᴇᴍʙᴇʀs.")

    user_mention = msg.from_user.mention if msg.from_user else "ʜɪᴅᴅᴇɴ ᴜsᴇʀ"
    status_msg = await msg.reply_text(f"» ᴜɴᴍᴜᴛᴇᴀʟʟ sᴛᴀʀᴛᴇᴅ ʙʏ {user_mention}")

    count = 0
    async for m in app.get_chat_members(chat_id, filter=enums.ChatMembersFilter.RESTRICTED):
        try:
            await app.restrict_chat_member(
                chat_id,
                m.user.id,
                ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_polls=True,
                    can_add_web_page_previews=True,
                    can_invite_users=True,
                    can_change_info=False,
                    can_pin_messages=False
                )
            )
            count += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except Exception as e:
            print(f"❌ {m.user.id if m.user else 'N/A'} - {e}")

    await status_msg.delete()
    
    if count == 0:
        await msg.reply_text("» ɴᴏ ᴍᴜᴛᴇᴅ ᴍᴇᴍʙᴇʀs ғᴏᴜɴᴅ.")
    else:
        await msg.reply_text(f"» ᴜɴᴍᴜᴛᴇᴅ {count} ᴍᴇᴍʙᴇʀs ɪɴ ᴛʜɪs ᴄʜᴀᴛ ✅")
        

@app.on_message(filters.command("banall") & filters.group)
async def banall_command(client, message):
    chat_id = message.chat.id

    me = await client.get_me()
    bot = await client.get_chat_member(chat_id, me.id)

    if not (bot.privileges and bot.privileges.can_restrict_members):
        return await message.reply_text(
            "» ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ʙᴀɴ ᴍᴇᴍʙᴇʀs!"
        )

    user_mention = message.from_user.mention if message.from_user else "ʜɪᴅᴅᴇɴ ᴜsᴇʀ"
    msg = await message.reply_text(f"» sᴛᴀʀᴛᴇᴅ ғᴜ*ᴋɪɴɢ ᴀʟʟ ᴍᴇᴍʙᴇʀs & ᴛʜᴇɪʀ ᴍᴏᴍs 😆 ʙʏ :- {user_mention}")

    count = 0
    user_id = message.from_user.id

    async for m in client.get_chat_members(chat_id):
        if not m.user:
            continue
        is_command_sender = (m.user.id == user_id)
        is_me = (m.user.id == me.id)
        
        if is_me or is_command_sender:
            continue  

        try:
            await client.ban_chat_member(chat_id, m.user.id)
            count += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except Exception:
            pass

    await msg.delete()
    await message.reply_text(
        f"» ʙᴀɴᴀʟʟ ᴄᴏᴍᴘʟᴇᴛᴇᴅ\n» ʙᴀɴɴᴇᴅ : {count} users")


@app.on_message(filters.command(["unpinall"]) & filters.group)
async def unpinall_command(client, message):
    chat = message.chat
    admin_id = message.from_user.id
    member = await chat.get_member(admin_id)

    user_permission = member.privileges.can_pin_messages if member.privileges else False

    if not user_permission:
        return await message.reply_text(
            "» ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴜɴᴘɪɴ ᴍᴇssᴀɢᴇs."
        )

    await message.reply_text(
        "» ᴀʀᴇ ʏᴏᴜ sᴜʀᴇ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴜɴᴘɪɴ ᴀʟʟ ᴘɪɴɴᴇᴅ ᴍᴇssᴀɢᴇs ɪɴ ᴛʜɪs ᴄʜᴀᴛ ??",
        reply_markup=InlineKeyboardMarkup(
            [[
                InlineKeyboardButton("✔ ʏᴇs", callback_data="unpin=yes"),
                InlineKeyboardButton("✖ ɴᴏ", callback_data="unpin=no")
            ]]
        )
    )



@app.on_message(filters.command("kickall") & filters.group)
async def kickall_command(client, message):
    chat_id = message.chat.id

    me = await client.get_me()
    bot = await client.get_chat_member(chat_id, me.id)

    if not (bot.privileges and bot.privileges.can_restrict_members):
        return await message.reply_text("» ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴋɪᴄᴋ ᴍᴇᴍʙᴇʀs.")

    user_mention = message.from_user.mention if message.from_user else "ʜɪᴅᴅᴇɴ ᴜsᴇʀ"
    msg = await message.reply_text(f"» ᴋɪᴄᴋᴀʟʟ sᴛᴀʀᴛᴇᴅ ʙʏ {user_mention}")
    
    count = 0
    user_id = message.from_user.id

    async for m in client.get_chat_members(chat_id):
        if not m.user:
            continue
        is_command_sender = (m.user.id == user_id)
        is_me = (m.user.id == me.id)
        
        if is_me or is_command_sender:
            continue  

        try:
            await client.ban_chat_member(chat_id, m.user.id)
            await client.unban_chat_member(chat_id, m.user.id)
            count += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except Exception:
            pass

    await msg.delete()
    await message.reply_text(f"» ᴋɪᴄᴋᴀʟʟ ᴄᴏᴍᴘʟᴇᴛᴇᴅ\n» ᴋɪᴄᴋᴇᴅ : {count}")


@app.on_message(filters.command("muteall") & filters.group)
async def muteall_command(client, message):
    chat_id = message.chat.id

    me = await client.get_me()
    bot = await client.get_chat_member(chat_id, me.id)

    if not (bot.privileges and bot.privileges.can_restrict_members):
        return await message.reply_text("» ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴍᴜᴛᴇ ᴍᴇᴍʙᴇʀs.")

    user_mention = message.from_user.mention if message.from_user else "ʜɪᴅᴅᴇɴ ᴜsᴇʀ"
    msg = await message.reply_text(f"» ᴍᴜᴛᴇᴀʟʟ sᴛᴀʀᴛᴇᴅ ʙʏ {user_mention}")
    
    count = 0
    user_id = message.from_user.id

    async for m in client.get_chat_members(chat_id):
        if not m.user:
            continue
        is_command_sender = (m.user.id == user_id)
        is_me = (m.user.id == me.id)
        
        if is_me or is_command_sender:
            continue

        try:
            await client.restrict_chat_member(
                chat_id,
                m.user.id,
                ChatPermissions(
                    can_send_messages=False,
                    can_send_media_messages=False,
                    can_send_polls=False,
                    can_add_web_page_previews=False,
                    can_invite_users=False,
                    can_change_info=False,
                    can_pin_messages=False
                )
            )
            count += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except Exception:
            pass

    await msg.delete()
    await message.reply_text(f"» ᴍᴜᴛᴇᴀʟʟ ᴄᴏᴍᴘʟᴇᴛᴇᴅ\n» ᴍᴜᴛᴇᴅ : {count}")


@app.on_callback_query(filters.regex(r"^unpin=(yes|no)$"))
async def unpin_callback(client, callback_query):
    chat_id = callback_query.message.chat.id
    user_id = callback_query.from_user.id
    action = callback_query.data.split("=")[1]

    if action == "yes":
        try:
            await client.unpin_all_chat_messages(chat_id)
            text = "» ᴀʟʟ ᴘɪɴɴᴇᴅ ᴍᴇssᴀɢᴇs ʜᴀᴠᴇ ʙᴇᴇɴ ᴜɴᴘɪɴɴᴇᴅ!"
        except Exception as e:
            text = f"» ᴇʀʀᴏʀ :- {e}"
    else:
        text = "» ᴏᴋᴀʏ, ɪ ᴡɪʟʟ ɴᴏᴛ ᴜɴᴘɪɴ ᴀɴʏᴛʜɪɴɢ."

    await callback_query.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")]]
        )
    )
