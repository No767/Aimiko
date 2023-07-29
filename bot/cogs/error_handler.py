import discord
from aimikocore import AimikoCore
from discord.app_commands import AppCommandError
from discord.ext import commands
from libs.utils import Embed, ErrorEmbed


class ErrorHandler(commands.Cog):
    def __init__(self, bot: AimikoCore) -> None:
        self.bot = bot

    async def cog_load(self) -> None:
        tree = self.bot.tree
        self._old_tree_error = tree.on_error
        tree.on_error = self.on_app_command_error

    async def cog_unload(self):
        tree = self.bot.tree
        tree.on_error = self._old_tree_error

    def full_exception(self, obj):
        module = obj.__class__.__module__
        if module is None or module == str.__class__.__module__:
            return obj.__class__.__name__
        return module + "." + obj.__class__.__name__

    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ) -> None:
        """Handles any errors on regular prefixed commands

        Args:
            ctx (commands.Context): Commands context
            error (commands.CommandError): The error that is being propagated
        """
        if isinstance(error, commands.CommandOnCooldown):
            seconds = int(error.retry_after) % (24 * 3600)
            hours = seconds // 3600
            seconds %= 3600
            minutes = seconds // 60
            seconds %= 60
            await ctx.send(
                embed=Embed(
                    description=f"This command is currently on cooldown. Try again in {hours} hour(s), {minutes} minute(s), and {seconds} second(s)."
                )
            )
        elif isinstance(error, commands.CommandNotFound):
            errorEmbed = ErrorEmbed()
            errorEmbed.title = "Command Not Found"
            errorEmbed.description = (
                "The command you were looking for could not be found"
            )
            await ctx.send(embed=errorEmbed)
        elif isinstance(error, commands.MissingRequiredArgument):
            errorEmbed = ErrorEmbed()
            errorEmbed.title = "Missing Required Argument"
            errorEmbed.description = (
                f"You are missing the following argument(s): {error.param.name}"
            )
            await ctx.send(embed=errorEmbed)
        else:
            errorEmbed = ErrorEmbed()
            errorEmbed.add_field(name="Error", value=str(error), inline=False)
            errorEmbed.add_field(
                name="Full Exception Message",
                value=f"{self.full_exception(error)}: {error}",
                inline=False,
            )
            await ctx.send(embed=errorEmbed)

    async def on_app_command_error(
        self, interaction: discord.Interaction, error: AppCommandError
    ):
        errorEmbed = ErrorEmbed()
        errorEmbed.add_field(name="Error", value=str(error), inline=False)
        errorEmbed.add_field(
            name="Full Exception Message",
            value=f"{self.full_exception(error)}: {error}",
            inline=False,
        )
        await interaction.response.send_message(embed=errorEmbed)


async def setup(bot: AimikoCore) -> None:
    await bot.add_cog(ErrorHandler(bot))
