import asyncpg

from database.models import User


class UserRepository:
    def __init__(self, host, port, database, user, password):
        self._host = host
        self._port = port
        self._database = database
        self._user = user
        self._password = password

    async def _get_connection(self):
        return await asyncpg.connect(
            host=self._host,
            port=self._port,
            database=self._database,
            user=self._user,
            password=self._password
        )

    async def create_table(self):
        conn = await self._get_connection()

        await conn.execute('''
        CREATE TABLE IF NOT EXISTS users(
        id TEXT PRIMARY KEY,
        full_name TEXT NOT NULL,
        role TEXT DEFAULT 'user',
        language TEXT DEFAULT 'en'
        )
        ''')

        await conn.close()

    async def save_entity(self, entity: User):
        conn = await self._get_connection()

        await conn.execute("INSERT INTO users (id, full_name, role, language) VALUES ($1, $2, $3)", (entity.id, entity.full_name, entity.role, entity.language))

        await conn.close()

    async def delete_entity(self, entity: User):
        conn = await self._get_connection()

        await conn.execute("DELETE FROM users WHERE id = ?", (entity.id,))

        await conn.close()

    async def get_entity(self, entity_id):
        conn = await self._get_connection()
        row = await conn.fetchone("SELECT * FROM entities WHERE id = ?", entity_id)
        await conn.close()
        if row:
            return User(id=row['id'], full_name=row['full_name'], role=row['role'], language=row['language'])
        else:
            return None
