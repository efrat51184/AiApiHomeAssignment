import asyncio
from fastapi import FastAPI
import uvicorn
from src.api.endpoints import router
from src.utils.async_utils import shutdown
import signal

app = FastAPI()
app.include_router(router)

loop = asyncio.get_event_loop()
for s in (signal.SIGINT, signal.SIGTERM):
    loop.add_signal_handler(s, lambda s=s: asyncio.create_task(shutdown(s, loop)))

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
