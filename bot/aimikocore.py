import logging
import signal
from pathlib import Path as SyncPath

import asyncpg
import discord
from aiohttp import ClientSession
from cogs import EXTENSIONS, VERSION
from discord.ext import commands
from libs.utils import AimikoHelp, ensure_pg_conn

# Some weird import logic to ensure that watchfiles is there
_fsw = True
try:
    from watchfiles import awatch
except ImportError:
    _fsw = False


def get_prefix(bot, msg: discord.Message):
    if msg.guild is None:
        return bot.default_prefix
    prefixes = ["?", "!", ">"]
    return prefixes


class AimikoCore(commands.Bot):
    """The core of Aimiko"""

    def __init__(
        self,
        intents: discord.Intents,
        session: ClientSession,
        pool: asyncpg.Pool,
        dev_mode: bool = False,
        *args,
        **kwargs,
    ):
        super().__init__(
            activity=discord.Activity(type=discord.ActivityType.watching, name=">help"),
            command_prefix=get_prefix,
            help_command=AimikoHelp(),
            intents=intents,
            owner_id=454357482102587393,
            *args,
            **kwargs,
        )
        self.dev_mode = dev_mode
        self._session = session
        self._pool = pool
        self._version = VERSION
        self.default_prefix = ">"
        self.logger = logging.getLogger("discord")

    @property
    def session(self) -> ClientSession:
        """A global web session used throughout the lifetime of the bot

        Returns:
            ClientSession: AIOHTTP ClientSession object
        """
        return self._session

    @property
    def pool(self) -> asyncpg.Pool:
        """A global object managed throughout the lifetime of bot

        Holds the asyncpg pool for connections

        Returns:
            asyncpg.Pool: asyncpg connection pool
        """
        return self._pool

    @property
    def version(self) -> str:
        """The current version of the bot

        Returns:
            str: Current version
        """
        parsed_version = f"{self._version.major}.{self._version.minor}.{self._version.micro}-{self._version.releaselevel}"
        return parsed_version

    async def fs_watcher(self) -> None:
        cogsPath = SyncPath(__file__).parent.joinpath("cogs")
        async for changes in awatch(cogsPath):
            changesList = list(changes)[0]
            if changesList[0].modified == 2:
                reloadFile = SyncPath(changesList[1])
                self.logger.info(f"Reloading extension: {reloadFile.name[:-3]}")
                await self.reload_extension(f"cogs.{reloadFile.name[:-3]}")

    async def setup_hook(self) -> None:
        def stop():
            self.loop.create_task(self.close())

        self.loop.add_signal_handler(signal.SIGTERM, stop)

        for cog in EXTENSIONS:
            self.logger.debug(f"Loaded extension: {cog}")
            await self.load_extension(cog)

        self.loop.create_task(ensure_pg_conn(self._pool))

        if self.dev_mode is True and _fsw is True:
            self.logger.info("Dev mode is enabled. Loading Jishaku and FSWatcher")
            self.loop.create_task(self.fs_watcher())
            await self.load_extension("jishaku")

    async def on_ready(self) -> None:
        if not hasattr(self, "uptime"):
            self.uptime = discord.utils.utcnow()
        curr_user = None if self.user is None else self.user.name
        self.logger.info(f"{curr_user} is fully ready!")
