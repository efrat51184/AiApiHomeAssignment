import asyncio
from asyncio import Semaphore

class AsyncRateLimiter:
    def __init__(self, max_rate: int, time_period: float):
        self.semaphore = Semaphore(max_rate)
        self.time_period = time_period

    async def __aenter__(self):
        await self.semaphore.acquire()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await asyncio.sleep(self.time_period)
        self.semaphore.release()
