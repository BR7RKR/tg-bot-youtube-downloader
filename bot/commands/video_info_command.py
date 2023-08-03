import re

from bot.commands.command import Command
from bot.commands.constants import Emojis
from bot.modules.inline_keyboard import InlineKeyboard, InlineKeyboardButton
from clients.tg import Update, TgClient
from utils.downloader import YouTubeDownloader


class VideoInfoCommand(Command):
    def __init__(self, tg_client: TgClient, downloader: YouTubeDownloader):
        self._tg_client = tg_client
        self._downloader = downloader

    async def execute(self, upd: Update):
        yt = self._downloader.get_video_info(upd.message.text)
        photo = yt.thumbnail_url
        vide_info = self._form_description(yt)
        reply_markup = self._form_reply_markup()
        await self._tg_client.send_photo(upd.message.chat.id, photo, vide_info, reply_markup)

    def is_for(self, command_definer: Update):
        if command_definer.message is None:
            return False

        url = command_definer.message.text
        url_pattern = re.compile(r'(https?://)?(www\.)?youtube\.com/watch\?v=([\w-]{11})(&.*)?$')
        return url_pattern.match(url)

    def _form_reply_markup(self) -> str:
        keyboard = InlineKeyboard()
        keyboard.add_button(button=InlineKeyboardButton(f"{Emojis.CAMERA.value}mp4", "button1"))
        keyboard.add_button(button=InlineKeyboardButton(f"{Emojis.SONG.value}mp3", "button2"))
        return keyboard.reply_markup

    def _form_description(self, yt) -> str:
        title = yt.title
        views = yt.views
        publish_date = str(yt.publish_date)[:-9]
        author = yt.author
        duration = yt.length
        vide_info = f"{title}\n{Emojis.EYE.value}{views}\n{Emojis.CALENDAR.value}{publish_date}\n{Emojis.MAN.value}{author}\n{Emojis.CLOCK_1.value}{duration}"
        return vide_info
