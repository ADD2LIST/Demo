# Author: Fayas (https://github.com/FayasNoushad) (@FayasNoushad)
from dotenv import load_dotenv

import ytthumb
from pyrogram import Client, Filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto

load_dotenv()

Bot = Client(
    "YouTube-Thumbnail-Downloader",
    bot_token="6296998029:AAHTHUXoqD-rXwk_EJmC84dMLt7yPp24qsk",
    api_id=21782827,
    api_hash="a12cbed580a87acc6d71ec4a53a3888f"
)

START_TEXT = """Hello {},
I am a simple YouTube thumbnail downloader Telegram bot.

- Send a YouTube video link or video ID.
- I will send the thumbnail.
- You can also send a YouTube video link or video ID with quality. (e.g., `rokGy0huYEA | sd`)
  - sd - Standard Quality
  - mq - Medium Quality
  - hq - High Quality
  - maxres - Maximum Resolution
"""

BUTTON = [InlineKeyboardButton("Feedback", url='https://telegram.me/Ad2list')]

photo_buttons = InlineKeyboardMarkup(
    [[InlineKeyboardButton('Other Qualities', callback_data='qualities')], BUTTON]
)

@Bot.on_callback_query()
async def cb_data(_, callback_query: CallbackQuery):
    data = callback_query.data.lower()
    message = callback_query.message
    if data == "qualities":
        await message.edit_text('Select a quality')
        buttons = []
        for quality in ytthumb.qualities():
            buttons.append(
                InlineKeyboardButton(
                    text=ytthumb.qualities()[quality],
                    callback_data=quality
                )
            )
        await message.edit_reply_markup(
            InlineKeyboardMarkup(
                [[buttons[0], buttons[1]], [buttons[2], buttons[3]], BUTTON]
            )
        )
    if data == "back":
        await message.edit_reply_markup(photo_buttons)
    if data in ytthumb.qualities():
        thumbnail = ytthumb.thumbnail(
            video=message.reply_to_message.text,
            quality=data
        )
        await Bot.send_message(
            chat_id=message.chat.id,
            text='Updating'
        )
        await message.edit_media(
            media=InputMediaPhoto(media=thumbnail),
            reply_markup=photo_buttons
        )
        await Bot.send_message(
            chat_id=message.chat.id,
            text='Update Successfully'
        )


@Bot.on_message(filters.private & filters.command(["start"]))
async def start(_, message):
    await message.reply_text(
        text=START_TEXT.format(message.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([BUTTON]),
        quote=True
    )


@Bot.on_message(filters.private & filters.text)
async def send_thumbnail(_, message):
    reply_message = await message.reply_text(
        text="Analyzing...",
        disable_web_page_preview=True,
        quote=True
    )
    try:
        if " | " in message.text:
            video = message.text.split(" | ", -1)[0]
            quality = message.text.split(" | ", -1)[1]
        else:
            video = message.text
            quality = "sd"
        thumbnail = ytthumb.thumbnail(
            video=video,
            quality=quality
        )
        await message.reply_photo(
            photo=thumbnail,
            reply_markup=photo_buttons,
            quote=True
        )
        await reply_message.delete()
    except Exception as error:
        await reply_message.edit_text(
            text=str(error),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([BUTTON])
        )


Bot.run()
