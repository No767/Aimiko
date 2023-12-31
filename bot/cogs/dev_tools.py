from typing import Literal, Optional

import discord
from aimikocore import AimikoCore
from discord.ext import commands
from discord.ext.commands import Context, Greedy


def is_nat():
    def pred(ctx):
        return (
            ctx.guild is not None and ctx.author.id == 1028431063321686036
        )  # natalie's account. This is Noelle's secondary testing account designed for testing Kumiko

    return commands.check(pred)


class DispatchFlags(commands.FlagConverter):
    guild: bool = commands.flag(
        default=True, description="Dispatch all guild related events"
    )
    member: bool = commands.flag(
        default=False, description="Dispatch all member related events"
    )


class DevTools(commands.Cog, command_attrs=dict(hidden=True)):
    """Tools for developing Kumiko"""

    def __init__(self, bot: AimikoCore):
        self.bot = bot

    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji(name="\U0001f6e0")

    @commands.hybrid_command(name="sync", with_app_command=False)
    @commands.guild_only()
    @commands.check_any(commands.is_owner(), is_nat())
    async def sync(
        self,
        ctx: Context,
        guilds: Greedy[discord.Object],
        spec: Optional[Literal["~", "*", "^"]] = None,
    ) -> None:
        """Performs a sync of the tree. This will sync, copy globally, or clear the tree.

        See this (https://about.abstractumbra.dev/discord.py/2023/01/29/sync-command-example.html) on how it works

        Args:
            ctx (Context): Context of the command
            guilds (Greedy[discord.Object]): Which guilds to sync to. Greedily accepts a number of guilds
            spec (Optional[Literal["~", "*", "^"], optional): Specs to sync.
        """
        await ctx.defer()
        if not guilds:
            if spec == "~":
                synced = await self.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                self.bot.tree.copy_global_to(guild=ctx.guild)  # type: ignore
                synced = await self.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                self.bot.tree.clear_commands(guild=ctx.guild)
                await self.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced = await self.bot.tree.sync()

            await ctx.send(
                f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
            )
            return

        ret = 0
        for guild in guilds:
            try:
                await self.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                ret += 1

        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

    @commands.check_any(commands.is_owner(), is_nat())
    @commands.guild_only()
    @commands.command(name="dispatch")
    async def dispatch(
        self, ctx: commands.Context, event: str, *, flags: DispatchFlags
    ) -> None:
        """Dispatch an event on the bot. Only really useful for testing"""
        if flags.guild:
            self.bot.dispatch(event, ctx.guild)
            await ctx.send(f"Dispatched `{event}` event")
            return

        if flags.member:
            self.bot.dispatch(event, ctx.guild, ctx.author)
            await ctx.send(f"Dispatched `{event}` event")
            return

        await ctx.send("Didn't dispatch event")
        return


async def setup(bot: AimikoCore) -> None:
    await bot.add_cog(DevTools(bot))
