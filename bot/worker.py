import asyncio
from typing import List

from bot.distributor import CommandDistributor
from clients.tg import TgClient
from clients.tg.dcs import Update


class Worker:
    def __init__(self, tg_client: TgClient, queue: asyncio.Queue, concurrent_workers: int):
        self.tg_client = tg_client
        self.queue = queue
        self.concurrent_workers = concurrent_workers
        self._tasks: List[asyncio.Task] = []
        self._command_distributor = CommandDistributor(tg_client=tg_client)

    async def handle_update(self, upd: Update):
        if self.tg_client is None:
            raise Exception('missing tg client')

        try:
            await self._command_distributor.execute(upd)
        except Exception as e:
            print(e)

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
