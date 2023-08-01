import os
import re

from bot.commands.command import Command
from clients.tg import UpdateObj
from utils.downloader import YouTubeDownloader


class DownloadAudioCommand(Command):
    def __init__(self, tg_client, downloader):
        self._tg_client = tg_client
        self._downloader = downloader

    async def execute(self, upd: UpdateObj):
        title = self._downloader.download_audio(url=upd.message.text)
        audio = open(f'audio/{title}', 'rb')
        try:
            await self._tg_client.send_audio(upd.message.chat.id, audio)
        except Exception as e:
            await self._tg_client.send_message(upd.message.chat.id, "Не получилось отправить видео")
        audio.close()
        os.remove(f'audio/{title}')

    def is_for(self, command_definer):
        url = command_definer
        url_pattern = re.compile(r'(https?://)?(www\.)?youtube\.com/watch\?v=([\w-]{11})(&.*)?$')
        return url_pattern.match(url)

