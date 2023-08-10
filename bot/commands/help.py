from bot.commands.command import Command
from bot.commands.constants import HELP_ANSWER
from clients.tg import Update


class HelpCommand(Command):
    def __init__(self, tg_client):
        self._name = "/help"
        self._tg_client = tg_client

    async def execute(self, upd: Update):
        await self._tg_client.send_message(upd.message.chat.id, HELP_ANSWER)

    def is_for(self, command_definer: Update):
        if command_definer.message is None:
            return False

        message = command_definer.message.text
        return self._name == message
