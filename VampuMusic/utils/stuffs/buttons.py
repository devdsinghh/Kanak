from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram import Client, filters, enums 
import config

class BUTTONS(object):
    ABUTTON = [
    [
        InlineKeyboardButton("sυᴘᴘᴏʀᴛ", url="https://t.me/kriti_supprot"),
        InlineKeyboardButton("υᴘᴅᴧᴛᴇs", url="https://t.me/kriti_update")
    ],
    [
        InlineKeyboardButton("ᴏᴡɴᴇʀ", user_id=config.OWNER_ID),
        InlineKeyboardButton("• ʙᴧᴄᴋ •", callback_data="settingsback_helper")
    ]
]

    INFO_BUTTON = [
    [
        InlineKeyboardButton("ʀєᴘσ", callback_data="gib_source"),
        InlineKeyboardButton("ʏᴛ-ᴀᴘɪ", callback_data="bot_info_data"),
        InlineKeyboardButton("ʟᴀɴɢᴜᴀɢᴇ", callback_data="LG"),
    ],
    [
        
        InlineKeyboardButton("ᴘʀɪᴠᴧᴄʏ", url="https://docs.google.com/document/d/11Q_ZuvSzkhkgbvVrPxQdqktP2_ioiaqAa7QdsHezfnM/mobilebasic"),
        InlineKeyboardButton("• ʙᴧᴄᴋ •", callback_data="settingsback_helper"),
    ]
    ]
    


    INFO_NEW = [
    [
        InlineKeyboardButton("• ʙᴧᴄᴋ •", callback_data="settings_back_helper")],
    ]
    
    
