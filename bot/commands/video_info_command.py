import re

from bot.commands.command import Command
from bot.commands.constants import Emojis
from clients.tg import UpdateObj, TgClient
from utils.downloader import YouTubeDownloader


class VideoInfoCommand(Command):
    def __init__(self, tg_client: TgClient, downloader: YouTubeDownloader):
        self._tg_client = tg_client
        self._downloader = downloader

    async def execute(self, upd: UpdateObj):
        yt = self._downloader.get_video_info(upd.message.text)
        photo = yt.thumbnail_url

        vide_info = self._form_description(yt)
        await self._tg_client.send_photo(upd.message.chat.id, photo, vide_info)

    def is_for(self, command_definer):
        url = command_definer
        url_pattern = re.compile(r'(https?://)?(www\.)?youtube\.com/watch\?v=([\w-]{11})(&.*)?$')
        return url_pattern.match(url)

    def _form_description(self, yt) -> str:
        title = yt.title
        views = yt.views
        publish_date = str(yt.publish_date)[:-9]
        author = yt.author
        duration = yt.length
        vide_info = f"{title}\n{Emojis.EYE.value}{views}\n{Emojis.CALENDAR.value}{publish_date}\n{Emojis.MAN.value}{author}\n{Emojis.CLOCK_1.value}{duration}"
        return vide_info
