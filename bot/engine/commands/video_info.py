import json
import re

from pytube import exceptions as pytube_ex

from clients.tg import TgClient, Update
from engine.commands.command import Command
from engine.commands.constants import YOUTUBE_LINK_PATTERN, Emojis
from engine.modules.inline_keyboard import InlineKeyboard, InlineKeyboardButton
from utils.downloaders import YouTubeDownloader


class VideoInfoCommand(Command):
    def __init__(self, tg_client: TgClient, downloader: YouTubeDownloader):
        self._tg_client = tg_client
        self._downloader = downloader
        self._url: str = ''

    async def execute(self, upd: Update):
        try:
            self._url = upd.message.text
            yt = self._downloader.get_video_info(self._url)
            photo = yt.thumbnail_url
            vide_info = self._form_description(yt)
            reply_markup = self._form_reply_markup()
            await self._tg_client.send_photo(upd.message.chat.id, photo, vide_info, reply_markup, True)
        except pytube_ex.VideoUnavailable as e:
            await self._tg_client.send_message(upd.message.chat.id, "Не получилось найти видео. Проверьте правильность ссылки.")
            return
        except Exception as e:
            await self._tg_client.send_message(upd.message.chat.id, "Не получилось отправить данные о видео")

    def is_for(self, command_definer: Update):
        if command_definer.message is None:
            return False

        url = command_definer.message.text
        url_pattern = re.compile(YOUTUBE_LINK_PATTERN)
        return url_pattern.match(url)

    def _form_reply_markup(self) -> str:
        keyboard = InlineKeyboard()
        match = re.search(YOUTUBE_LINK_PATTERN, self._url)
        id = match.group(1)
        video_data = {"type": "video", "data": f"{id}"}
        audio_data = {"type": "audio", "data": f"{id}"}
        keyboard.add_button(button=InlineKeyboardButton(f"{Emojis.CAMERA.value}mp4", json.dumps(video_data)))
        keyboard.add_button(button=InlineKeyboardButton(f"{Emojis.SONG.value}mp3", json.dumps(audio_data)))
        return keyboard.reply_markup

    def _form_description(self, yt) -> str:
        title = yt.title
        views = yt.views
        publish_date = str(yt.publish_date)[:-9]
        author = yt.author
        duration = yt.length
        vide_info = f"{title}\n{Emojis.EYE.value}{views}\n{Emojis.CALENDAR.value}{publish_date}\n{Emojis.MAN.value}{author}\n{Emojis.CLOCK_1.value}{duration}s"
        return vide_info
