import asyncio
import os
import signal
import discord
from config.logging_config import *
from commands.general_commands import GeneralCommands
from discord.ext import commands
from enums.errors import allowed_errors
from dotenv import load_dotenv
from tasks.voice_channel import process_messages, message_queue


load_dotenv()
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
intents = discord.Intents.default()
intents.message_content = True

class OtaBot(commands.Bot):
    async def setup_hook(self):
        self.bg_task = asyncio.create_task(
            process_messages(
                self,
                message_queue,
            )
        )


bot = OtaBot(command_prefix=".", intents=intents)
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

    logging.error(exception)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)

    if not message.content.startswith("."):
        if message_queue.full():
            _ = await message_queue.get()

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
