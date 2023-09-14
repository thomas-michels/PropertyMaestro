import asyncio
import uvicorn

from app.scheduler import app as app_rocketry


class Server(uvicorn.Server):
    def handle_exit(self, sig: int, frame) -> None:
        app_rocketry.session.shut_down()
        return super().handle_exit(sig, frame)


async def start_application():
    sched = asyncio.create_task(app_rocketry.serve())

    await asyncio.wait([sched])
