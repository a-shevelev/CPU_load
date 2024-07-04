import asyncio

from aiohttp import web
import aiohttp_cors
from app.settings import config
from app.database.models import postgres_accessor


async def setup_tasks(application):
   from app.cpu.load_func import save_cpu_load
   application['cpu_load_task'] = asyncio.create_task(save_cpu_load())
def setup_accessors(application):
   application['db'] = postgres_accessor
   application['db'].setup(application)

def setup_routes(application):
   from app.cpu.routes import setup_routes as setup_forum_routes
   setup_forum_routes(application)

def setup_config(application):
   application["config"] = config



def setup_app(application):
   setup_config(application)
   setup_accessors(application)
   setup_routes(application)
   for route in list(app.router.routes()):
      cors.add(route)


   application.on_startup.append(setup_tasks)

app = web.Application()

cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
        allow_credentials=True,
        expose_headers="*",
        allow_headers="*",
        allow_methods="*",  # Добавьте методы, которые используются в ваших представлениях
    )
})

if __name__ == "__main__":
   setup_app(app)

   web.run_app(app, port=config["common"]["port"])