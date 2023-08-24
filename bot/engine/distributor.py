# import bot.engine.commands as commands

from clients.tg import Update
from utils.downloaders import YouTubeDownloader
from engine.commands import TestCommand, DownloadAudioCommand, DownloadVideoCommand, VideoInfoCommand, HelpCommand, Command


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

    # def set_commands(self):
    #     command_list = []
    #     for cls in commands.__dict__.values():
    #         if isinstance(cls, type) and issubclass(cls, commands.Command) and cls.__name__ == "Command":
    #             command_list.append(cls())
    #
    #     return command_list


    async def execute(self, upd: Update):
        command = await self._define_command(upd)

        if command is None:
            return

        try:
            await command.execute(upd)
        except Exception as e:
            print(e)
            return

    async def _define_command(self, command_definer) -> Command:
        for com in self._commands:
            if com.is_for(command_definer):
                return com

