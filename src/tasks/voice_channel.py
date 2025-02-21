import logging
import os
import asyncio
import discord
from dotenv import load_dotenv

load_dotenv()
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
message_queue = asyncio.Queue(maxsize=100)


async def process_messages(bot, message_queue):
    while True:
        message = await message_queue.get()
        voice_channel = message.author.voice.channel
        bot_voice_channel = message.guild.voice_client

        try:
            general_commands = bot.get_cog("GeneralCommands")
            if bot_voice_channel and general_commands.enabled_to_speak_messages and message.content:
                if voice_channel == bot_voice_channel.channel:
                    tts_audio_path = "tts_audio.mp3"
                    text_to_say = message.content

                    os.system(
                        f"gtts-cli '{text_to_say}' --lang {general_commands.current_language} --output {tts_audio_path}"
                    )

                    if os.path.exists(tts_audio_path):
                        bot_voice_channel.play(
                            discord.FFmpegPCMAudio(tts_audio_path),
                            after=lambda e: logging.debug("Audio finished"),
                        )

                        while bot_voice_channel.is_playing():
                            await asyncio.sleep(1)

                        os.remove(tts_audio_path)
        except Exception as err:
            logging.error(err)
            if ENVIRONMENT == "development":
                await message.channel.send(err)
                return
            await message.channel.send(
                "An error occurred while trying to speak the message."
            )
        finally:
            message_queue.task_done()
