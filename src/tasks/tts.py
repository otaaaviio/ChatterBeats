import logging
import os
import asyncio
import discord
from dotenv import load_dotenv
from enums.languages import LanguageManager
from tasks.queues import message_queue

load_dotenv()
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")


async def process_tts(message):
    try:
        curr_lang = LanguageManager.get_language().value

        voice_channel = message.author.voice.channel
        bot_voice_channel = message.guild.voice_client
        if bot_voice_channel and message.content:
            is_same_channel = (
                voice_channel and voice_channel == bot_voice_channel.channel
            )
            is_same_chat = message.channel == bot_voice_channel.channel
            if is_same_channel and is_same_chat:
                tts_audio_path = "tts_audio.mp3"
                text_to_say = message.content

                os.system(
                    f"gtts-cli '{text_to_say}' --lang {curr_lang} --output {tts_audio_path}"
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
