import sys
from pathlib import Path

import discord
import discord.ext.test as dpytest
import pytest
import pytest_asyncio
from discord.ext import commands

path = Path(__file__).parents[2].joinpath("bot")
sys.path.append(str(path))

from libs.utils import ConfirmEmbed, Embed, ErrorEmbed


class EmbedCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="embed-test")
    async def embed_test(self, ctx: commands.Context) -> None:
        embed = Embed(title="Hi")
        await ctx.send(embed=embed)

    @commands.command(name="embed-error")
    async def embed_error(self, ctx: commands.Context) -> None:
        embed = ErrorEmbed()
        await ctx.send(embed=embed)

    @commands.command(name="embed-confirm")
    async def embed_confirm(self, ctx: commands.Context) -> None:
        embed = ConfirmEmbed()
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


@pytest.mark.asyncio
async def test_error_embed(bot):
    embed = ErrorEmbed()
    await dpytest.message(">embed-error")
    assert dpytest.verify().message().embed(embed=embed)


@pytest.mark.asyncio
async def test_confirm_embed(bot):
    embed = ConfirmEmbed()
    await dpytest.message(">embed-confirm")
    assert dpytest.verify().message().embed(embed=embed)
