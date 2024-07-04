from datetime import datetime

from aiohttp import web


class PostgresAccessor:
    def __init__(self) -> None:
        self.db = None

    def setup(self, application: web.Application) -> None:
        application.on_startup.append(self._on_connect)
        application.on_cleanup.append(self._on_disconnect)

    async def _on_connect(self, application: web.Application):
        from app.database.models import db
        timestamp_now = datetime.now()


        self.config = application["config"]["postgres"]
        await db.set_bind(self.config["database_url"])
        self.db = db
        from app.cpu.models import CPULoad, ServerStatus
        async with self.db.transaction():
            await ServerStatus.create(status="START", timestamp=timestamp_now)
            # await CPULoad.create(timestamp=timestamp_now, load=0)
        print(f"Saved server status: START")

    async def _on_disconnect(self, _) -> None:
        from app.database.models import db
        timestamp_now = datetime.now()
        if self.db is not None:
            from app.cpu.models import CPULoad, ServerStatus
            async with self.db.transaction():
                await ServerStatus.create(status="STOP", timestamp=timestamp_now)
                # await CPULoad.create(timestamp=timestamp_now, load=0)
                print(f"Saved server status: STOP")
            await self.db.pop_bind().close()