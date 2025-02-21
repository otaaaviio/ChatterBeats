import asyncio
import os
import signal
import discord
from config.logging_config import *
from commands.general_commands import GeneralCommands
from discord.ext import commands
from enums.errors import allowed_errors
from dotenv import load_dotenv

load_dotenv()
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

intents = discord.Intents.all()
message_queue = asyncio.Queue()


class MyBot(commands.Bot):
    async def setup_hook(self):
        self.bg_task = asyncio.create_task(process_messages())


bot = MyBot(command_prefix=".", intents=intents)
general_commands = GeneralCommands(bot)


@bot.event
async def on_ready():
    await bot.add_cog(general_commands)
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
    
    print(ctx)

    logging.error(exception)


async def process_messages():
    while True:
        message = await message_queue.get()
        voice_channel = message.author.voice.channel
        bot_voice_channel = message.guild.voice_client

        try:
            if (
                bot_voice_channel
                and general_commands.enabled_to_speak_messages
                and message.content
            ):
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


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith("."):
        await bot.process_commands(message)
        return

    await message_queue.put(message)

async def shutdown():
    if bot.voice_clients:
        for vc in bot.voice_clients:
            await vc.disconnect()
    await bot.close()
    
def handle_exit(sig, frame):
    asyncio.get_event_loop().create_task(shutdown())

async def main():
    DISCORD_API_TOKEN = os.getenv("DISCORD_API_TOKEN")
    signal.signal(signal.SIGINT, handle_exit)
    await bot.start(DISCORD_API_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
