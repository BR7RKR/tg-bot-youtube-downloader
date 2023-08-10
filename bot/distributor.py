from bot.commands.command import Command
from bot.commands.download_audio import DownloadAudioCommand
from bot.commands.download_video import DownloadVideoCommand
from bot.commands.help import HelpCommand
from bot.commands.test import TestCommand
from bot.commands.video_info import VideoInfoCommand
from clients.tg import Update
from utils.downloader import YouTubeDownloader


class CommandDistributor:
    def __init__(self, tg_client):
        self._youtube_downloader = YouTubeDownloader()

        self._commands = {
            TestCommand(tg_client=tg_client),
            DownloadAudioCommand(tg_client=tg_client, downloader=self._youtube_downloader),
            DownloadVideoCommand(tg_client=tg_client, downloader=self._youtube_downloader),
            VideoInfoCommand(tg_client=tg_client, downloader=self._youtube_downloader),
            HelpCommand(tg_client=tg_client)
        }

    async def execute(self, upd: Update):
        command = await self._define_command(upd)
        try:
            await command.execute(upd)
        except Exception as e:
            print(e)
            return

    async def _define_command(self, command_definer) -> Command:
        for com in self._commands:
            if com.is_for(command_definer):
                return com

