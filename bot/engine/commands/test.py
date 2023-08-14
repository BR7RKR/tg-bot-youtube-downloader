from clients.tg import Update
from engine.commands.command import Command


class TestCommand(Command):
    def __init__(self, tg_client):
        self._name = "/test"
        self._tg_client = tg_client

    async def execute(self, upd: Update):
        await self._tg_client.send_message(upd.message.chat.id, upd.message.text)

    def is_for(self, command_definer: Update):
        if command_definer.message is None:
            return False

        message = command_definer.message.text
        return self._name == message
