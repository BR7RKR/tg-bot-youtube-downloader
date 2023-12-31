import json
import os
import re

import aiofiles
from pytube.exceptions import VideoUnavailable

from clients.tg import CallBackData, TgClient
from engine.constants import YOUTUBE_PREFIX, HELP_ANSWER, YOUTUBE_LINK_PATTERN, Emojis, START_ANSWER
from engine.modules.keyboards import InlineKeyboard, InlineKeyboardButton
from abc import ABCMeta, abstractmethod

from clients.tg import Update
from utils.downloaders import YouTubeDownloader
from utils.formatters import TimeFormatter


# Abstract command
class Command:
    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self, upd: Update):
        pass

    @abstractmethod
    def is_for(self, command_definer: Update):
        pass


class DownloadAudioCommand(Command):
    def __init__(self, tg_client: TgClient, downloader: YouTubeDownloader):
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
            await self._tg_client.send_message(upd.callback_query.message.chat.id, "Не получилось отправить аудио")
        finally:
            await file.close()
            keyboard = InlineKeyboard()
            await self._tg_client.edit_message_reply_markup(upd.callback_query.message.chat.id,
                                                            upd.callback_query.message.message_id,
                                                            reply_markup=keyboard.reply_markup)
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


class DownloadVideoCommand(Command):
    def __init__(self, tg_client: TgClient, downloader: YouTubeDownloader):
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


class HelpCommand(Command):
    def __init__(self, tg_client: TgClient):
        self._name = "/help"
        self._tg_client = tg_client

    async def execute(self, upd: Update):
        await self._tg_client.send_message(upd.message.chat.id, HELP_ANSWER)

    def is_for(self, command_definer: Update):
        if command_definer.message is None:
            return False

        message = command_definer.message.text
        return self._name == message


class TestCommand(Command):
    def __init__(self, tg_client: TgClient):
        self._name = "/test"
        self._tg_client = tg_client

    async def execute(self, upd: Update):
        await self._tg_client.send_message(upd.message.chat.id, upd.message.text)

    def is_for(self, command_definer: Update):
        if command_definer.message is None:
            return False

        message = command_definer.message.text
        return self._name == message


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
        except VideoUnavailable as e:
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
        duration = TimeFormatter.format_time(yt.length)
        vide_info = f"{title}\n{Emojis.EYE.value}{views}\n{Emojis.CALENDAR.value}{publish_date}\n{Emojis.MAN.value}{author}\n{Emojis.CLOCK_1.value}{duration}"
        return vide_info


class StartCommand(Command):
    def __init__(self, tg_client: TgClient):
        self._name = "/start"
        self._tg_client = tg_client

    async def execute(self, upd: Update):
        await self._tg_client.send_message(upd.message.chat.id, START_ANSWER)

    def is_for(self, command_definer: Update):
        if command_definer.message is None:
            return False

        message = command_definer.message.text
        return self._name == message
