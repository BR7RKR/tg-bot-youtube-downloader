import json
import os

import aiofiles

from clients.tg import Update, CallBackData
from engine.commands.command import Command
from engine.commands.constants import YOUTUBE_PREFIX
from engine.modules.inline_keyboard import InlineKeyboard


class DownloadVideoCommand(Command):
    def __init__(self, tg_client, downloader):
        self._tg_client = tg_client
        self._downloader = downloader
        self._url = YOUTUBE_PREFIX

    async def execute(self, upd: Update):
        title = self._downloader.download_video(self._url)
        self._url = YOUTUBE_PREFIX
        file = await aiofiles.open(f'video/{title}', 'rb')
        try:
            video = await file.read()
            await self._tg_client.send_video(upd.callback_query.message.chat.id, video)
        except Exception as e:
            await self._tg_client.send_message(upd.callback_query.message.chat.id, "Не получилось отправить видео")
        finally:
            await file.close()
            keyboard = InlineKeyboard()
            await self._tg_client.edit_message_reply_markup(upd.callback_query.message.chat.id,
                                                            upd.callback_query.message.message_id,
                                                            reply_markup=keyboard.reply_markup)
            os.remove(f'video/{title}')

    def is_for(self, command_definer: Update):
        if command_definer.callback_query is None:
            return False
        data: str = command_definer.callback_query.data
        data_json = json.loads(data)
        data_obj: CallBackData = CallBackData.Schema().load(data_json)
        if data_obj.type == 'video':
            self._url += data_obj.data
            return True
        return False
