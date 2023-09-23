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

        async with conn.transaction():
            await conn.execute('''
            CREATE TABLE IF NOT EXISTS users(
            id TEXT PRIMARY KEY,
            username TEXT NOT NULL,
            firstname TEXT NOT NULL,
            lastname TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            language TEXT DEFAULT 'en'
            )
            ''')

        await conn.close()

    async def save_entity(self, entity: User):
        conn = await self._get_connection()

        async with conn.transaction():
            await conn.execute("INSERT INTO users (id, username, firstname, lastname, role, language) VALUES ($1, $2, $3, $4, $5, $6)",
                               entity.id, entity.username, entity.firstname, entity.lastname, entity.role, entity.language)

        await conn.close()

    async def delete_entity(self, entity: User):
        conn = await self._get_connection()

        async with conn.transaction():
            await conn.execute("DELETE FROM users WHERE id = ($1)", entity.id)

        await conn.close()

    async def get_entity(self, entity_id):
        conn = await self._get_connection()

        async with conn.transaction():
            row = await conn.fetchrow("SELECT * FROM users WHERE id = ($1)", entity_id)

        await conn.close()
        if row:
            return User(id=row['id'], username=row['username'], firstname=row['firstname'], lastname=row['lastname'], role=row['role'], language=row['language'])
        else:
            return None
