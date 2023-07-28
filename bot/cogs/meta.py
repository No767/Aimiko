from aikocore import AikoCore
from discord.ext import commands
from libs.utils import time


class Meta(commands.Cog):
    """Commands that provide information about Aiko"""

    def __init__(self, bot: AikoCore) -> None:
        self.bot = bot

    def get_bot_uptime(self, *, brief: bool = False) -> str:
        return time.human_timedelta(
            self.bot.uptime, accuracy=None, brief=brief, suffix=False
        )

    @commands.hybrid_command(name="uptime")
    async def uptime(self, ctx: commands.Context) -> None:
        """Shows the uptime of the bot"""
        await ctx.send(f"Uptime: **{self.get_bot_uptime()}**")


async def setup(bot: AikoCore) -> None:
    await bot.add_cog(Meta(bot))
