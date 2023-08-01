import os
import re

from bot.commands.command import Command
from clients.tg import UpdateObj


class DownloadAudioCommand(Command):
    def __init__(self, tg_client, downloader):
        self._tg_client = tg_client
        self._downloader = downloader

    async def execute(self, upd: UpdateObj):
        title = self._downloader.download_video(url=upd.message.text)
        video = open(f'video/{title}', 'rb')
        try:
            await self._tg_client.send_video(upd.message.chat.id, video)
        except Exception as e:
            await self._tg_client.send_message(upd.message.chat.id, "Не получилось отправить видео")
        video.close()
        os.remove(f'video/{title}')

    def is_for(self, command_definer):
        if type(command_definer) is UpdateObj:
            if command_definer.callback_query is not None:
                return command_definer.callback_query.data['button'] == 'button1'
        return False
