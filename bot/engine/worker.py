import asyncio
from typing import List

from bot.clients.tg import TgClient, Update
from bot.engine.distributor import CommandDistributor
from bot.engine.exceptions import MissingTgClientError


class Worker:
    def __init__(self, tg_client: TgClient, queue: asyncio.Queue, concurrent_workers: int):
        self.tg_client = tg_client
        self.queue = queue
        self.concurrent_workers = concurrent_workers
        self._tasks: List[asyncio.Task] = []
        self._command_distributor = CommandDistributor(tg_client=tg_client)

    async def handle_update(self, upd: Update):
        if self.tg_client is None:
            raise MissingTgClientError(Worker.__name__)

        await self._command_distributor.execute(upd)

    async def _worker(self):
        while True:
            upd = await self.queue.get()
            try:
                await self.handle_update(upd)
            finally:
                self.queue.task_done()

    async def start(self):
        self._tasks = [asyncio.create_task(self._worker()) for _ in range(self.concurrent_workers)]

    async def stop(self):
        await self.queue.join()
        for t in self._tasks:
            t.cancel()