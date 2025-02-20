import asyncio
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import discord
from src.logging_config import *
from src.commands import BotCommands
from discord.ext import commands
from enums.errors import allowed_errors
from dotenv import load_dotenv

load_dotenv()
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=".", intents=intents)
bot_commands = BotCommands(bot)


@bot.event
async def on_ready():
    await bot.add_cog(bot_commands)
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.playing, name=".otabot")
    )
    print(f"bot working: {bot.user} in {ENVIRONMENT} mode")


@bot.event
async def on_command_error(ctx, exception):
    if ENVIRONMENT == "development":
        await ctx.send(exception)
        return

    if type(exception) in allowed_errors:
        await ctx.send(exception)
        return

    logging.error(exception)


@bot.event
async def on_message(message):
    if message.author == bot.user :
        return

    await bot.process_commands(message)
    
    if message.content.startswith("."):
        return

    voice_channel = message.author.voice.channel
    bot_voice_channel = message.guild.voice_client

    if bot_voice_channel and bot_commands.enabled_to_speak_messages:
        if voice_channel == bot_voice_channel.channel:
            try:
                print(f"{message.author}")
                tts_audio_path = "tts_audio.mp3"
                text_to_say =  message.content

                os.system(
                    f"gtts-cli '{text_to_say}' --lang pt --output {tts_audio_path}"
                )

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


def main():
    DISCORD_API_TOKEN = os.getenv("DISCORD_API_TOKEN")
    bot.run(DISCORD_API_TOKEN)


if __name__ == "__main__":
    main()
