from io import IOBase
from typing import Optional, Union, List, Dict

import aiohttp
from aiohttp import FormData

from clients.tg import UpdateType
from clients.tg.dcs import GetUpdatesResponse, SendMessageResponse, SendAudioResponse, SendPhotoResponse, \
    SendVideoResponse


class TgClient:
    def __init__(self, token: str = ''):
        self.token = token

    def get_url(self, method: str):
        return f"https://api.telegram.org/bot{self.token}/{method}"

    async def get_me(self) -> dict:
        url = self.get_url("getMe")
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                return await resp.json()

    async def get_updates(self, offset: Optional[int] = None, timeout: int = 0) -> dict:
        url = self.get_url("getUpdates")
        params = {}
        if offset:
            params['offset'] = offset
        if timeout:
            params['timeout'] = timeout
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as resp:
                return await resp.json()

    async def get_updates_in_objects(self, offset: Optional[int] = None, timeout: int = 0) -> GetUpdatesResponse:
        res_dict = await self.get_updates(offset=offset, timeout=timeout)
        return GetUpdatesResponse.Schema().load(res_dict)

    async def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        url = self.get_url("sendMessage")
        payload = {
            'chat_id': chat_id,
            'text': text
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as resp:
                res_dict = await resp.json()
                return SendMessageResponse.Schema().load(res_dict)

    async def send_audio(self, chat_id: int, audio: Union[IOBase, str]) -> SendAudioResponse:
        url = self.get_url("sendAudio")
        data = FormData()
        data.add_field('chat_id', str(chat_id))
        data.add_field('audio', audio)
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data) as resp:
                res_dict = await resp.json()
                return SendAudioResponse.Schema().load(res_dict)

    async def send_video(self, chat_id: int, video: Union[IOBase, str]) -> SendVideoResponse:
        url = self.get_url("sendVideo")
        data = FormData()
        data.add_field('chat_id', str(chat_id))
        data.add_field('video', video)
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data) as resp:
                res_dict = await resp.json()
                return SendVideoResponse.Schema().load(res_dict)

    async def send_photo(self, chat_id: int, photo: Union[IOBase, str], caption: Optional[str] = None, reply_markup: Optional = None) -> SendPhotoResponse:
        url = self.get_url("sendPhoto")
        data = FormData()
        data.add_field('chat_id', str(chat_id))
        data.add_field('photo', photo)

        if caption is not None:
            data.add_field('caption', caption)
        if reply_markup is not None:
            data.add_field('reply_markup', reply_markup)

        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data) as resp:
                res_dict = await resp.json()
                return SendPhotoResponse.Schema().load(res_dict)
