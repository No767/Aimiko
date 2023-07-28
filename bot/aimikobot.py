import asyncio
import os

import asyncpg
import discord
from aimikocore import AimikoCore
from aiohttp import ClientSession
from dotenv import load_dotenv
from libs.utils import AimikoLogger

try:
    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass

load_dotenv()

TOKEN = os.environ["TOKEN"]
DEV_MODE = os.getenv("DEV_MODE") in ("True", "TRUE")
POSTGRES_URI = os.environ["POSTGRES_URI"]

intents = discord.Intents.default()
intents.message_content = True


async def main() -> None:
    async with ClientSession() as session, asyncpg.create_pool(
        dsn=POSTGRES_URI, command_timeout=60, max_size=20, min_size=20
    ) as pool:
        async with AimikoCore(
            intents=intents, session=session, pool=pool, dev_mode=DEV_MODE
        ) as bot:
            await bot.start(TOKEN)


def launch() -> None:
    with AimikoLogger():
        asyncio.run(main())


if __name__ == "__main__":
    try:
        launch()
    except KeyboardInterrupt:
        pass
