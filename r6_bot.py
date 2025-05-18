from keep_alive import keep_alive
from r6bot import config, events, commands as bot_commands
import discord
import threading
import time
import requests
from discord.ext import commands

# Load Opus library for voice support 
discord.opus.load_opus('libopus.so.0')
print("Opus loaded:", discord.opus.is_loaded())

# Keep-alive for hosting stuff
keep_alive()

def self_ping():
    while True:
        try:
            requests.get("https://bfee465e-510d-4680-8a28-dca6401f1dfa-00-3fv41izmqv8r8.worf.replit.dev/")
            print("Self-pinged successfully")
        except Exception as e:
            print("Self-ping failed:", e)
        time.sleep(280)

threading.Thread(target=self_ping, daemon=True).start()

# bot and command tree setup
intents = config.get_intents()
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree  # Access the CommandTree from the bot

# register events and slash commands BEFORE syncing
events.register(bot)
bot_commands.register(tree)

@bot.event
async def on_ready():
    await tree.sync()
    print(f"✅ Bot is online as {bot.user} and slash commands synced.")

# Start the bot
bot.run(config.BOT_TOKEN)