import discord
from aimikocore import AimikoCore
from discord import app_commands
from discord.ext import commands
from discord.utils import utcnow
from libs.ui.prefix import DeletePrefixView
from libs.utils import ConfirmEmbed, Embed, PrefixConverter, get_prefix, is_manager


class Prefix(commands.Cog):
    """Utilities to manage and view your server prefixes"""

    def __init__(self, bot: AimikoCore) -> None:
        self.bot = bot
        self.pool = self.bot.pool

    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji(name="\U000025b6")

    @commands.guild_only()
    @commands.hybrid_group(name="prefix", fallback="list")
    async def prefix(self, ctx: commands.Context) -> None:
        """Allows you to manage your server prefixes

        If a subcommand is not called, then this will return the list of prefixes for your server
        """
        prefixes = await get_prefix(self.bot, ctx.message)
        cleaned = ", ".join([f"`{prefix}`" for prefix in prefixes]).rstrip(",")
        embed = Embed(description=f"**Current prefixes**\n{cleaned}")
        embed.timestamp = utcnow()
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon.url)  # type: ignore
        await ctx.send(embed=embed)

    @is_manager()
    @commands.guild_only()
    @prefix.command(name="add")
    @app_commands.describe(prefix="The new prefix to add")
    async def add(self, ctx: commands.Context, prefix: PrefixConverter) -> None:
        """Adds new prefixes into your server"""
        prefixes = await get_prefix(self.bot, ctx.message)
        if len(prefixes) > 10:
            desc = "There was an validation issue. This is because of two reasons:\n- You have more than 10 prefixes for your server\n- Your prefix fails the validation rules"
            raise RuntimeError(desc)

        if prefix in self.bot.prefixes[ctx.guild.id]:  # type: ignore
            await ctx.send("The prefix you want to set already exists")
            return

        query = """
            UPDATE guild
            SET prefix = ARRAY_APPEND(prefix, $1)
            WHERE id=$2;
        """
        guild_id = ctx.guild.id  # type: ignore
        await self.pool.execute(query, prefix, guild_id)
        if isinstance(self.bot.prefixes[guild_id], list):
            self.bot.prefixes[guild_id].append(prefix)
        else:
            self.bot.prefixes[guild_id] = [self.bot.default_prefix, prefix]
        await ctx.send(f"Added prefix: `{prefix}`")

    @is_manager()
    @commands.guild_only()
    @prefix.command(name="update")
    @app_commands.describe(
        old_prefix="The old prefix to replace", new_prefix="The new prefix to use"
    )
    async def update(
        self, ctx: commands.Context, old_prefix: str, new_prefix: PrefixConverter
    ) -> None:
        """Updates the prefix for your server"""
        query = """
            UPDATE guild
            SET prefix = ARRAY_REPLACE(prefix, $1, $2)
            WHERE id = $3;
        """
        guild_id = ctx.guild.id  # type: ignore
        if old_prefix in self.bot.prefixes[guild_id]:
            await self.pool.execute(query, old_prefix, new_prefix, guild_id)
            prefixes = self.bot.prefixes[guild_id][
                :
            ]  # Shallow copy the list so we can safely perform operations on it
            for idx, item in enumerate(prefixes):
                if item == old_prefix:
                    prefixes[idx] = new_prefix
            self.bot.prefixes[guild_id] = prefixes
            await ctx.send(f"Prefix updated to `{new_prefix}`")
        else:
            await ctx.send("The prefix is not in the list of prefixes for your server")

    @is_manager()
    @commands.guild_only()
    @prefix.command(name="delete", aliases=["remove"])
    @app_commands.describe(prefix="The prefix to delete")
    async def deletePrefixes(self, ctx: commands.Context, prefix: str) -> None:
        """Deletes a prefix from your server"""
        view = DeletePrefixView(bot=self.bot, prefix=prefix)
        embed = ConfirmEmbed()
        embed.description = f"Do you want to delete the following prefix: `{prefix}`"
        await ctx.send(embed=embed, view=view)


async def setup(bot: AimikoCore) -> None:
    await bot.add_cog(Prefix(bot))
