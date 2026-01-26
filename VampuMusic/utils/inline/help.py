from typing import Union

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from VampuMusic import app


def help_pannel(_, START: Union[bool, int] = None):
    first = [InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")]
    second = [
        InlineKeyboardButton(
            text=_["BACK_BUTTON"],
            callback_data="settingsback_helper",
        ),
    ]
    mark = second if START else first

    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["H_B_25"],
                    callback_data="help_callback hb1",
                ),
                InlineKeyboardButton(
                    text=_["H_B_26"],
                    callback_data="help_callback hb2",
                ),
                InlineKeyboardButton(
                    text=_["H_B_28"],
                    callback_data="help_callback hb3",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["H_B_27"],
                    callback_data="help_callback hb4",
                ),
                InlineKeyboardButton(
                    text=_["H_B_31"],
                    callback_data="help_callback hb5",
                ),
                InlineKeyboardButton(
                    text=_["H_B_29"],
                    callback_data="help_callback hb6",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["H_B_33"],
                    callback_data="help_callback hb7",
                ),
                InlineKeyboardButton(
                    text=_["H_B_30"],
                    callback_data="help_callback hb8",
                ),
                InlineKeyboardButton(
                    text=_["H_B_32"],
                    callback_data="help_callback hb9",
                ),
            ],

            [
                InlineKeyboardButton(
                    text="• ᴀᴄᴛɪᴏɴ •",
                    callback_data="ban_cb",
                ),
                InlineKeyboardButton(
                    text="• ᴍᴏᴅᴇʀᴀᴛɪᴏɴ •",
                    callback_data="mod_cb",
                ),
                InlineKeyboardButton(
                    text="• sᴇᴛᴜᴘ •",
                    callback_data="setup_cb",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="• ᴡᴇʟᴄᴏᴍᴇ •",
                    callback_data="wel_cb",
                ),
                InlineKeyboardButton(
                    text="• ᴠᴄ-ʟᴏɢɢᴇʀ •",
                    callback_data="vc_cb",
                ),
                InlineKeyboardButton(
                    text="• ᴘʀᴏᴍᴏᴛᴇ •",
                    callback_data="ad_cb",
                ),
            ],

            mark,
        ]
    )
    return upl


def help_back_markup(_):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["BACK_BUTTON"],
                    callback_data=f"settings_back_helper",
                ),
            ]
        ]
    )
    return upl


def private_help_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_4"],
                url=f"https://t.me/{app.username}?start=help",
            ),
        ],
    ]
    return buttons

