import re

from bot.commands.command import Command
from clients.tg import UpdateObj, TgClient
from utils.downloader import YouTubeDownloader


class VideoInfoCommand(Command):
    def __init__(self, tg_client: TgClient, downloader: YouTubeDownloader):
        self._tg_client = tg_client
        self._downloader = downloader

    async def execute(self, upd: UpdateObj):
        yt = self._downloader.get_video_info(upd.message.text)
        photo = yt.thumbnail_url
        await self._tg_client.send_photo(upd.message.chat.id, photo)

    def is_for(self, command_definer):
        url = command_definer
        url_pattern = re.compile(r'(https?://)?(www\.)?youtube\.com/watch\?v=([\w-]{11})(&.*)?$')
        return url_pattern.match(url)
