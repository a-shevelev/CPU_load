from aiohttp import web
from aiohttp_cors import CorsViewMixin

from app.cpu.models import CPULoad
from app.cpu.load_func import get_cpu_load_last_hour, get_average_load_per_minute


class ListCPULoadView(web.View, CorsViewMixin):
    async def get(self):
        cpu_loads = await CPULoad.query.order_by(CPULoad.id.desc()).gino.all()
        cpu_load_data = []
        for cpu_load in cpu_loads:
            cpu_load_data.append(
                {
                    "id": cpu_load.id,
                    "timestamp": str(cpu_load.timestamp),
                    "load": cpu_load.load,
                },
            )
        return web.json_response(data={"cpu_load": cpu_load_data})

class GetCPULoadLastHourView(web.View, CorsViewMixin):
    async def get(self):
        cpu_loads = await get_cpu_load_last_hour()
        cpu_load_data = []
        for cpu_load in cpu_loads:
            cpu_load_data.append(
                {
                    "id": cpu_load.id,
                    "timestamp": str(cpu_load.timestamp),
                    "load": cpu_load.load,
                }
            )
        return web.json_response(data={"cpu_load": cpu_load_data})


class GetCPULoadLastHourPerMinuteView(web.View, CorsViewMixin):
    async def get(self):
        cpu_loads = await get_average_load_per_minute()
        cpu_load_data = []
        for timestamp, cpu_load in cpu_loads.items():
            cpu_load_data.append(
                {
                    "timestamp": str(timestamp),
                    "load": cpu_load,
                }
            )
        return web.json_response(data={"cpu_load": cpu_load_data})