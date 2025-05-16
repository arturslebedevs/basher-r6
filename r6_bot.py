from keep_alive import keep_alive
from discord.ext import commands
from r6bot import config, events

keep_alive()

bot = commands.Bot(command_prefix="!", intents=config.get_intents())


@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")


events.register(bot)
bot.run(config.BOT_TOKEN)
