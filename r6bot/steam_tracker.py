import aiohttp
import asyncio
import os
from dotenv import load_dotenv
import discord
from r6bot import config

# Load API key from .env
load_dotenv()
STEAM_API_KEY = os.getenv("STEAM_API_KEY")

# Steam users to track
STEAM_USERS = {
    "Kārlis": {
        "steamid": "76561198982317073", 
        "discord_id": 930045752670027776  
    },
    "barbeque3": {
        "steamid": "76561198086014989",  
        "discord_id": 520958179643883520
    },
}

# Game IDs
TARGET_GAMES = {
    359550: "Tom Clancy's Rainbow Six Siege",
    730: "Counter-Strike: Global Offensive",
}

# Track user states
current_games = {}

async def get_current_game(steamid):
    url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={steamid}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            players = data.get("response", {}).get("players", [])
            if not players:
                return None
            return players[0].get("gameid")

async def poll_steam_games(bot):
    await bot.wait_until_ready()
    while not bot.is_closed():
        for name, user in STEAM_USERS.items():
            steamid = user["steamid"]
            discord_id = user["discord_id"]
            new_game_id = await get_current_game(steamid)
            old_game_id = current_games.get(steamid)

            if new_game_id != old_game_id:
                channel = discord.utils.get(bot.get_all_channels(), name=config.CHANNEL_NAME)
                if channel:
                    member = channel.guild.get_member(discord_id)
                    if not member:
                        continue

                    if new_game_id and int(new_game_id) in TARGET_GAMES:
                        game_name = TARGET_GAMES[int(new_game_id)]
                        await channel.send(f"🎮 {member.mention} started playing **{game_name}**")
                    elif old_game_id and int(old_game_id) in TARGET_GAMES:
                        game_name = TARGET_GAMES[int(old_game_id)]
                        await channel.send(f"🚫 {member.mention} stopped playing **{game_name}**")

            current_games[steamid] = new_game_id

        await asyncio.sleep(30)