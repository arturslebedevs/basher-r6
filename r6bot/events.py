import random
import discord
from r6bot import config, messages


def register(bot):

    # Gamin events
    @bot.event
    async def on_presence_update(before, after):
        before_game = before.activity.name if before.activity else None
        after_game = after.activity.name if after.activity else None

        for guild in bot.guilds:
            if after.id not in [m.id for m in guild.members]:
                continue

            channel = discord.utils.get(guild.text_channels,
                                        name=config.CHANNEL_NAME)
            if not channel:
                continue

            is_karlis = after.name == "Kārlis"

            # Started playing something
            if after_game and after_game != before_game:
                print(f"🕹️ {after.name} started playing {after_game}")

                if is_karlis:
                    if after_game == config.TARGET_GAME_R6:
                        msg = random.choice(
                            messages.karlis_sweaty_messages).format(
                                user=after.mention)
                        await channel.send(msg)
                    elif after_game == config.TARGET_GAME_CS2:
                        msg = random.choice(
                            messages.karlis_cs2_messages).format(
                                user=after.mention)
                        await channel.send(msg)
                else:
                    if after_game == config.TARGET_GAME_R6:
                        msg = random.choice(messages.sweaty_messages).format(
                            user=after.mention)
                        await channel.send(msg)

            # Stopped playing R6
            if before_game == config.TARGET_GAME_R6 and (
                    after.activity is None
                    or after.activity.name != config.TARGET_GAME_R6):
                print(f"🛑 {after.name} stopped playing R6 Siege")

                if is_karlis:
                    msg = random.choice(
                        messages.karlis_redemption_messages).format(
                            user=after.mention)
                else:
                    msg = random.choice(messages.redemption_messages).format(
                        user=after.mention)

                await channel.send(msg)

    # If bot is mentioned
    @bot.event
    async def on_message(message):
        if message.author.bot:
            return  # ignore bots

        if bot.user in message.mentions:
            if message.author.name == "barbeque3":
                await message.channel.send("🫡 yes my lord")
            else:
                await message.channel.send("🖕 Atpisies")

        await bot.process_commands(message)
