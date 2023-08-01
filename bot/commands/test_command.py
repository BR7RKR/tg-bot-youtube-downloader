from bot.commands.command import Command
from clients.tg import UpdateObj


class TestCommand(Command):
    def __init__(self, tg_client):
        self._name = "/test"
        self._tg_client = tg_client

    async def execute(self, upd: UpdateObj):
        await self._tg_client.send_message(upd.message.chat.id, upd.message.text)

    def is_for(self, command_definer):
        message = command_definer
        return self._name == message
