import aiohttp
import asyncio
import os
from dotenv import load_dotenv
import discord
import random
from r6bot import config, messages
from r6bot.utils import weighted_random_message 

# Load API key from .env
load_dotenv()
STEAM_API_KEY = os.getenv("STEAM_API_KEY")

# Steam users to track
STEAM_USERS = {
    "ROBINGHOOD": {
        "steamid": "76561198982317073",
        "discord_id": 930045752670027776,
        "label": "Kārlis"
    },
    "barbeque3": {
        "steamid": "76561198086014989",
        "discord_id": 520958179643883520,
        "label": "barbeque3"
    },
    "ChengaljenG": {
        "steamid": "76561198342529465",
        "discord_id": 351349100991741953,
        "label": "kRITEX"
    },
    "Grim": {
        "steamid": "76561198118135486",
        "discord_id": 396343528927526928,
        "label": "Harijs be like"
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

                    label = user.get("label", name)
                    is_karlis = label == "Kārlis"

                    # STARTED PLAYING
                    if new_game_id and int(new_game_id) in TARGET_GAMES:
                        game_name = TARGET_GAMES[int(new_game_id)]
                        print(f"[Steam] {name} started playing {game_name}")

                        if int(new_game_id) == 359550:  # R6
                            if is_karlis:
                                msg = random.choice(messages.karlis_sweaty_messages).format(user=member.mention)
                                await channel.send(msg)
                            else:
                                selected_msg = weighted_random_message(
                                    messages.sweaty_messages,
                                    messages.extra_russian_sweaty_messages,
                                    base_weight=1,
                                    extra_weight=9
                                )
                                msg = selected_msg.format(user=member.mention)
                                await channel.send(msg)
                                if selected_msg in messages.extra_russian_sweaty_messages:
                                    file = discord.File("assets/img/russian_suffering.png")
                                    await channel.send(file=file)
                        elif int(new_game_id) == 730:  # CS2
                            if is_karlis:
                                msg = random.choice(messages.karlis_cs2_messages).format(user=member.mention)
                                await channel.send(msg)

                    # STOPPED PLAYING
                    elif old_game_id and int(old_game_id) == 359550 and not new_game_id:  # R6 stopped
                        print(f"[Steam] {name} stopped playing R6")
                        if is_karlis:
                            msg = random.choice(messages.karlis_redemption_messages).format(user=member.mention)
                        else:
                            msg = random.choice(messages.redemption_messages).format(user=member.mention)
                        await channel.send(msg)

            current_games[steamid] = new_game_id

        await asyncio.sleep(30)