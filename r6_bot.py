from keep_alive import keep_alive
from discord.ext import commands
from r6bot import config, events
import discord  
import threading
import time
import requests

discord.opus.load_opus('libopus.so.0')
print("Opus loaded:", discord.opus.is_loaded())  

keep_alive()

def self_ping():
    while True:
        try:
            requests.get("https://bfee465e-510d-4680-8a28-dca6401f1dfa-00-3fv41izmqv8r8.worf.replit.dev/")
            print("Self-pinged successfully")
        except Exception as e:
            print("Self-ping failed:", e)
        time.sleep(280)  # every ~4.6 minutes

threading.Thread(target=self_ping, daemon=True).start()

bot = commands.Bot(command_prefix="!", intents=config.get_intents())


@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")


events.register(bot)
bot.run(config.BOT_TOKEN)