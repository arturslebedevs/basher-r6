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

                # Wait until actually connected (max 3s)
                for _ in range(30):
                    if vc.is_connected():
                        break
                    await asyncio.sleep(0.1)

                if not vc.is_connected():
                    raise RuntimeError("VC connect timeout")

                ffmpeg_path = "ffmpeg"
                # Start FFmpeg process manually for deeper control
                process = subprocess.Popen(
                    [ffmpeg_path, "-i", "assets/moan.mp3", "-f", "s16le", "-ar", "48000", "-ac", "2", "pipe:1"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )

                if not process or not process.stdout:
                    print("❌ Failed to start ffmpeg process.")
                    return

                audio_source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(process.stdout))

                print("🔊 Attempting to play moan.mp3")
                vc.play(audio_source)
                print("🎵 Play command issued")

                # Wait briefly for playback to start
                for _ in range(10):
                    if vc.is_playing():
                        break
                    await asyncio.sleep(0.1)

                if not vc.is_playing():
                    print("❌ Playback failed, disconnecting")
                    await asyncio.sleep(0.2)

                    stderr_output, _ = process.communicate()
                    print("🔻 FFmpeg stderr:")
                    print(stderr_output.decode(errors="ignore"))

                    await vc.disconnect()
                    return

                while vc.is_playing():
                    await asyncio.sleep(1)

                await vc.disconnect()
                print("👋 Left VC after playing")

            except Exception as e:
                print(f"❗️ Error joining VC: {repr(e)}")

    @bot.event
    async def on_presence_update(before, after):
        before_game = before.activity.name if before.activity else None
        after_game = after.activity.name if after.activity else None

        for guild in bot.guilds:
            if after.id not in [m.id for m in guild.members]:
                continue

            channel = discord.utils.get(guild.text_channels, name=config.CHANNEL_NAME)
            if not channel:
                continue

            is_karlis = after.name == "Kārlis"

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

            if before_game == config.TARGET_GAME_R6 and (
                after.activity is None or after.activity.name != config.TARGET_GAME_R6):
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