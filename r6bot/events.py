import random
import asyncio
import discord
import subprocess  
from r6bot import config, messages

def register(bot):

    @bot.event
    async def on_voice_state_update(member, before, after):
        if before.channel is None and after.channel is not None:
            vc_channel = after.channel

            try:
                if member.guild.voice_client:
                    vc = member.guild.voice_client
                else:
                    vc = await vc_channel.connect()

                # Wait until connected
                for _ in range(30):
                    if vc.is_connected():
                        break
                    await asyncio.sleep(0.1)

                if not vc.is_connected():
                    raise RuntimeError("VC connect timeout")

                ffmpeg_path = "ffmpeg"
                audio_source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(
                    "assets/moan.mp3",
                    executable=ffmpeg_path,
                    before_options="-nostdin",
                    options="-vn",
                    stderr=subprocess.PIPE  
                ))

                print("🔊 Attempting to play moan.mp3")
                vc.play(audio_source)
                print("🎵 Play command issued")

                # Wait for playback to start
                for _ in range(10):
                    if vc.is_playing():
                        break
                    await asyncio.sleep(0.1)

                if not vc.is_playing():
                    print("Playback failed, disconnecting")
                    await asyncio.sleep(0.2)

                    if audio_source._process:
                        err = await asyncio.to_thread(audio_source._process.stderr.read)
                        print("FFmpeg stderr:")
                        print(err.decode(errors="ignore"))

                    await vc.disconnect()
                    return

                while vc.is_playing():
                    await asyncio.sleep(1)

                await vc.disconnect()
                print("Left VC after playing")

            except Exception as e:
                print(f"Error joining VC: {repr(e)}")

    @bot.event
    async def on_presence_update(before, after):
        def get_game_name(user):
            for activity in user.activities:
                if isinstance(activity, discord.Game):
                    return activity.name
            return None

        before_game = get_game_name(before)
        after_game = get_game_name(after)

        for guild in bot.guilds:
            if after.id not in [m.id for m in guild.members]:
                continue

            channel = discord.utils.get(guild.text_channels, name=config.CHANNEL_NAME)
            if not channel:
                continue

            is_karlis = after.name == "Kārlis"

            # Started playing
            if after_game and after_game != before_game:
                print(f"🕹️ {after.name} started playing {after_game}")

                if is_karlis:
                    if after_game == config.TARGET_GAME_R6:
                        msg = random.choice(messages.karlis_sweaty_messages).format(user=after.mention)
                        await channel.send(msg)
                    elif after_game == config.TARGET_GAME_CS2:
                        msg = random.choice(messages.karlis_cs2_messages).format(user=after.mention)
                        await channel.send(msg)
                else:
                    if after_game == config.TARGET_GAME_R6:
                        msg = random.choice(messages.sweaty_messages).format(user=after.mention)
                        await channel.send(msg)

            # Stopped playing R6
            if before_game == config.TARGET_GAME_R6 and after_game != config.TARGET_GAME_R6:
                await asyncio.sleep(10)  
                confirmed_game = get_game_name(after)
                if confirmed_game == config.TARGET_GAME_R6:
                    print(f"⚠️ False R6 exit detected for {after.name}, still playing.")
                    return

                print(f"🛑 {after.name} stopped playing R6 Siege")

                if is_karlis:
                    msg = random.choice(messages.karlis_redemption_messages).format(user=after.mention)
                else:
                    msg = random.choice(messages.redemption_messages).format(user=after.mention)

                await channel.send(msg)

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