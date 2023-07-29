import discord
from aimikocore import AimikoCore
from discord.ext import commands


class EventsHandler(commands.Cog):
    """Cog to handle all events"""

    def __init__(self, bot: AimikoCore) -> None:
        self.bot = bot
        self.pool = self.bot.pool

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild) -> None:
        # We can do an upsert in here instead
        # Someone remind me to change this later
        exists_query = """
        SELECT EXISTS(SELECT 1 FROM guild WHERE id = $1);
        """
        insert_query = """
        INSERT INTO guild (id)
        VALUES ($1);
        """
        async with self.pool.acquire() as conn:
            exists = await conn.fetchval(exists_query, guild.id)
            if not exists:
                await conn.execute(insert_query, guild.id)
                self.bot.prefixes[guild.id] = None

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild) -> None:
        delete_query = """
        DELETE FROM guild WHERE id = $1;
        """
        await self.pool.execute(delete_query, guild.id)
        if guild.id in self.bot.prefixes[guild.id]:
            del self.bot.prefixes[guild.id]


async def setup(bot: AimikoCore):
    await bot.add_cog(EventsHandler(bot))
