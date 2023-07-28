import discord
from aimikocore import AimikoCore
from discord.ext import commands
from libs.utils import time


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


async def setup(bot: AimikoCore) -> None:
    await bot.add_cog(Meta(bot))
