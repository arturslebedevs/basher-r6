import os
import discord
from dotenv import load_dotenv

load_dotenv()  

BOT_TOKEN = os.getenv("BOT_TOKEN")
TARGET_GAME_R6 = "Tom Clancy's Rainbow Six Siege"
TARGET_GAME_CS2 = "Counter-Strike 2"
CHANNEL_NAME = "💬enneeleee💬"  

def get_intents():
    intents = discord.Intents.default()
    intents.presences = True
    intents.members = True
    intents.guilds = True
    return intents