from discord import app_commands, Interaction
from r6bot.version import BOT_VERSION

def register(tree: app_commands.CommandTree):
    @tree.command(name="version", description="Show the bot version")
    async def version_command(interaction: Interaction):
        await interaction.response.send_message(f"Current fentabot version: `{BOT_VERSION}`")

    @tree.command(name="help", description="Show a list of available commands")
    async def help_command(interaction: Interaction):
        help_text = (
            "**Available Commands:**\n"
            "• `/version` — Show the current bot version\n"
            "• `/help` — Show this help message\n"
        )
        await interaction.response.send_message(help_text, ephemeral=True)