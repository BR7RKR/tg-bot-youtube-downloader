import json
import os

import aiofiles

from bot.commands.command import Command
from bot.commands.constants import YOUTUBE_PREFIX
from clients.tg import Update, CallBackData


class DownloadAudioCommand(Command):
    def __init__(self, tg_client, downloader):
        self._tg_client = tg_client
        self._downloader = downloader
        self._url = YOUTUBE_PREFIX

    async def execute(self, upd: Update):
        title = self._downloader.download_audio(self._url)
        self._url = YOUTUBE_PREFIX
        file = await aiofiles.open(f'audio/{title}', 'rb')
        try:
            audio = await file.read()
            await self._tg_client.send_audio(upd.callback_query.message.chat.id, audio)
        except Exception as e:
            await self._tg_client.send_message(upd.message.chat.id, "Не получилось отправить аудио")
        finally:
            await file.close()
            os.remove(f'audio/{title}')

    def is_for(self, command_definer: Update):
        if command_definer.callback_query is None:
            return False
        data: str = command_definer.callback_query.data
        data_json = json.loads(data)
        data_obj: CallBackData = CallBackData.Schema().load(data_json)
        if data_obj.type == 'audio':
            self._url += data_obj.data
            return True
        return False


