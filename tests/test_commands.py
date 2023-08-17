from unittest.mock import MagicMock, AsyncMock

import pytest

from clients.tg import TgClient, Update, Message, MessageFrom, Chat
from engine.commands import HelpCommand


class TestHelpCommand:
    @pytest.fixture
    @pytest.mark.asyncio
    def setup(self, monkeypatch):
        self.mock_tg_client = AsyncMock(spec=TgClient)
        monkeypatch.setattr('engine.commands.TgClient', MagicMock(return_value=self.mock_tg_client))
        self.command = HelpCommand(tg_client=self.mock_tg_client)
        return self

    @pytest.mark.asyncio
    async def test_is_for_works_properly(self, setup):
        #arrange
        update = Update(update_id=12)
        message_from = MessageFrom(id=1, first_name="John", last_name="Doe", username="johndoe")
        chat = Chat(id=1, type="private", first_name="John", last_name="Doe", username="johndoe")
        update.message = Message(message_id=1, from_=message_from, chat=chat, text="/help")
        #act
        result = self.command.is_for(update)
        #assert
        assert result == True
