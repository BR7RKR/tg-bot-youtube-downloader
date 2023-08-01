from bot.commands.command import Command
from bot.commands.download_audio_command import DownloadAudioCommand
from bot.commands.test_command import TestCommand
from bot.commands.video_info_command import VideoInfoCommand
from clients.tg import UpdateObj
from utils.downloader import YouTubeDownloader


class CommandDistributor:
    def __init__(self, tg_client):
        self._youtube_downloader = YouTubeDownloader()

        self._commands = {
            TestCommand(tg_client=tg_client),
            #DownloadAudioCommand(tg_client=tg_client, downloader=self._youtube_downloader),
            VideoInfoCommand(tg_client=tg_client, downloader=self._youtube_downloader)
        }

    async def execute(self, upd: UpdateObj):
        command = await self._define_command(upd.message.text)
        await command.execute(upd)

    async def _define_command(self, command_definer) -> Command:
        for com in self._commands:
            if com.is_for(command_definer):
                return com

