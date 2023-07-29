import platform

import discord
from aimikocore import AimikoCore
from discord.ext import commands
from libs.utils import Embed, time


class Meta(commands.Cog):
    """Commands that provide information about Aiko"""

    def __init__(self, bot: AimikoCore) -> None:
        self.bot = bot

    def get_bot_uptime(self, *, brief: bool = False) -> str:
        return time.human_timedelta(
            self.bot.uptime, accuracy=None, brief=brief, suffix=False
        )

    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji(name="\U00002754")

    @commands.hybrid_command(name="uptime")
    async def uptime(self, ctx: commands.Context) -> None:
        """Shows the uptime of the bot"""
        await ctx.send(f"Uptime: **{self.get_bot_uptime()}**")

    @commands.hybrid_command(name="version")
    async def version(self, ctx: commands.Context) -> None:
        """Shows the version of Aimiko"""
        await ctx.send(f"Build Version: {self.bot.version}")

    @commands.hybrid_command(name="info")
    async def info(self, ctx: commands.Context) -> None:
        """Shows the info of the bot"""
        embed = Embed()
        embed.title = f"{self.bot.user.name} Info"  # type: ignore
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)  # type: ignore
        embed.add_field(name="Server Count", value=len(self.bot.guilds), inline=True)
        embed.add_field(name="User Count", value=len(self.bot.users), inline=True)
        embed.add_field(
            name="Python Version", value=platform.python_version(), inline=True
        )
        embed.add_field(
            name="Discord.py Version", value=discord.__version__, inline=True
        )
        embed.add_field(
            name="Aimiko Build Version", value=self.bot.version, inline=True
        )
        await ctx.send(embed=embed)


async def setup(bot: AimikoCore) -> None:
    await bot.add_cog(Meta(bot))
