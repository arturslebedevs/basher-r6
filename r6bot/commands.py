from discord.ext import commands
from r6bot.version import BOT_VERSION

def register(bot: commands.Bot):
    @bot.command(name="version")
    async def version_command(ctx):
        await ctx.send(f"Current fentabot version: `{BOT_VERSION}`")