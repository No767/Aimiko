import sys
from pathlib import Path

import discord
import discord.ext.test as dpytest
import pytest
import pytest_asyncio
from discord.ext import commands

path = Path(__file__).parents[2].joinpath("bot")
sys.path.append(str(path))

from libs.utils import Embed


class EmbedCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="embed-test")
    async def embed_test(self, ctx: commands.Context) -> None:
        embed = Embed(title="Hi")
        await ctx.send(embed=embed)


@pytest_asyncio.fixture
async def bot():
    # Setup
    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True
    b = commands.Bot(command_prefix=">", intents=intents)
    await b._async_setup_hook()  # setup the loop
    await b.add_cog(EmbedCog(b))

    dpytest.configure(b)

    yield b

    # Teardown
    await dpytest.empty_queue()


@pytest.mark.asyncio
async def test_embed_content(bot):
    embed = Embed(title="Hi")
    await dpytest.message(">embed-test")
    assert dpytest.verify().message().embed(embed=embed)
