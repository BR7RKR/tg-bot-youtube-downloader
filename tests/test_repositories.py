import pytest

from database.models import User
from database.repositories import UserRepository


class TestUserRepository:
    @pytest.fixture
    def setup(self):
        self._repo = UserRepository(host="localhost",
                                    port=5432,
                                    database="postgres",
                                    user="postgres",
                                    password="mysecretpassword")
        return self

    @pytest.mark.asyncio
    async def test_get_entity_works_fine(self, setup): #TODO: реализовать тестирование без опоры на лишний функционал
        #arrange
        id = 'test'
        expected = User(id, 'test', 'test', 'test', 'user', 'en')
        await self._repo.save_entity(expected)
        #act
        res = await self._repo.get_entity(id)
        #assert
        await self._repo.delete_entity(expected.id)
        assert res == expected
