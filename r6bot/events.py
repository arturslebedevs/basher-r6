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

    # Voice state update for ANY user
        @bot.event
        async def on_voice_state_update(member, before, after):
            if before.channel is None and after.channel is not None:
                vc_channel = after.channel

                try:
                    # If bot is already connected, skip connecting again
                    if member.guild.voice_client:
                        vc = member.guild.voice_client
                    else:
                        vc = await vc_channel.connect()

                    audio_source = discord.FFmpegPCMAudio("assets/moan.mp3")
                    if not vc.is_playing():
                        vc.play(audio_source)

                        # Wait while playing
                        while vc.is_playing():
                            await discord.sleep(1)

                        await vc.disconnect()

                except Exception as e:
                    print(f"Error joining VC: {e}")
