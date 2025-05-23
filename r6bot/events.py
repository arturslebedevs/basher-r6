import random
import asyncio
import discord
import subprocess
from r6bot import config, messages
from r6bot.steam_tracker import STEAM_USERS
from r6bot.utils import weighted_random_message
STEAM_USER_IDS = [user["discord_id"] for user in STEAM_USERS.values()]


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
                    "assets/audio/moan.mp3",
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
        if after.id in STEAM_USER_IDS:
            return  # Steam handles it

        def get_game_name(user):
            for activity in user.activities:
                print(f"[DEBUG] Activity for {user.name}: {activity}")
                if isinstance(activity, discord.Game):
                    return activity.name
            return None

        before_game = get_game_name(before)
        after_game = get_game_name(after)
        print(f"[DEBUG] {before.name} activities: {before.activities}")
        print(f"[DEBUG] {after.name} activities: {after.activities}")

        for guild in bot.guilds:
            if after.id not in [m.id for m in guild.members]:
                continue

            channel = discord.utils.get(guild.text_channels, name=config.CHANNEL_NAME)
            if not channel:
                print(f"[WARN] Channel '{config.CHANNEL_NAME}' not found in guild '{guild.name}'")
                continue

            is_karlis = after.name == "Kārlis"

            # Started playing
            if after_game and after_game != before_game:
                print(f"🔹 {after.name} started playing {after_game}")

                if is_karlis:
                    if after_game == config.TARGET_GAME_R6:
                        msg = random.choice(messages.karlis_sweaty_messages).format(user=after.mention)
                        await channel.send(msg)
                    elif after_game == config.TARGET_GAME_CS2:
                        msg = random.choice(messages.karlis_cs2_messages).format(user=after.mention)
                        await channel.send(msg)
                else:
                    if after_game == config.TARGET_GAME_R6:
                        selected_msg = weighted_random_message(
                            messages.sweaty_messages,
                            messages.extra_russian_sweaty_messages,
                            base_weight=3,
                            extra_weight=1
                        )
                        msg = selected_msg.format(user=after.mention)
                        await channel.send(msg)

                        # If the selected raw message came from the extra list, send image
                        if selected_msg in messages.extra_russian_sweaty_messages:
                            file = discord.File("assets/img/russian_suffering.png")
                            await channel.send(file=file)

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
            return

        if bot.user in message.mentions:
            if message.author.name == "barbeque3":
                await message.channel.send("🫡 yes my lord")
            else:
                await message.channel.send("🖕 Atpisies")

        await bot.process_commands(message)
