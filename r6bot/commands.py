import discord
from discord import app_commands
from r6bot.version import BOT_VERSION

def register(bot: discord.Client):
    tree = app_commands.CommandTree(bot)

    @tree.command(name="version", description="Show the current bot version")
    async def version_command(interaction: discord.Interaction):
        await interaction.response.send_message(f"Current fentabot version: `{BOT_VERSION}`")

    # Sync commands 
    @bot.event
    async def on_ready():
        await tree.sync()
        print("Slash commands synced.")