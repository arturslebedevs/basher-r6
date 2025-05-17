from discord import app_commands, Interaction
from r6bot.version import BOT_VERSION

def register(tree: app_commands.CommandTree):
    @tree.command(name="version", description="Show the bot version")
    async def version_command(interaction: Interaction):
        await interaction.response.send_message(f"🤖 Current fentabot version: `{BOT_VERSION}`")