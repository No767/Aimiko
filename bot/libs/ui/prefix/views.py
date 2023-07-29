import discord
from aimikocore import AimikoCore
from libs.utils import ErrorEmbed, SuccessActionEmbed


class DeletePrefixView(discord.ui.View):
    def __init__(self, bot: AimikoCore, prefix: str) -> None:
        super().__init__()
        self.bot = bot
        self.prefix = prefix
        self.pool = self.bot.pool

    @discord.ui.button(
        label="Confirm",
        style=discord.ButtonStyle.green,
        emoji="<:greenTick:596576670815879169>",
    )
    async def confirm(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        query = """
        UPDATE guild
        SET prefix = ARRAY_REMOVE(prefix, $1)
        WHERE id=$2;
        """
        curr_guild = interaction.guild
        if curr_guild is None:
            self.clear_items()
            embed = ErrorEmbed(
                title="You are not in a guild",
                description="You are running this command within a DM or GC. This is not supported",
            )
            await interaction.response.edit_message(embed=embed, view=self)
            return
        guild_id = curr_guild.id
        # We will only delete it if the prefix is in the list of prefixes
        # This ensures that the prefix **must** be in the LRU cache
        if self.prefix in self.bot.prefixes[guild_id]:
            await self.pool.execute(query, self.prefix, guild_id)
            self.bot.prefixes[guild_id].remove(
                self.prefix
            )  # This makes the assumption that the guild is already in the LRU cache
            self.clear_items()
            embed = SuccessActionEmbed(
                description=f"The prefix `{self.prefix}` was successfully removed"
            )
            await interaction.response.edit_message(embed=embed, view=self)
            return
        else:
            self.clear_items()
            embed = ErrorEmbed(
                title="Prefix not found",
                description=f"The prefix `{self.prefix}` was not found",
            )
            await interaction.response.edit_message(embed=embed, view=self)
            return

    @discord.ui.button(
        label="Cancel",
        style=discord.ButtonStyle.red,
        emoji="<:redTick:596576672149667840>",
    )
    async def cancel(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        await interaction.response.defer()
        await interaction.delete_original_response()
        self.stop()
