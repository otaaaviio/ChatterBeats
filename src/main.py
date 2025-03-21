import asyncio
import os
import signal
import discord
from config.logging_config import *
from discord.ext import commands
from dotenv import load_dotenv
from tasks.process_messages import process_messages
from events.events import setup_events


load_dotenv()
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
intents = discord.Intents.default()
intents.message_content = True


class ChatterBeats(commands.Bot):
    async def setup_hook(self):
        self.bg_task = asyncio.create_task(process_messages())


bot = ChatterBeats(command_prefix=".", intents=intents)
setup_events(bot)


async def shutdown():
    if bot.voice_clients:
        for vc in bot.voice_clients:
            await vc.disconnect()
    await bot.close()
    await bot.http.close()


def handle_exit(sig, frame):
    asyncio.get_event_loop().create_task(shutdown())


async def main():
    DISCORD_API_TOKEN = os.getenv("DISCORD_API_TOKEN")
    signal.signal(signal.SIGINT, handle_exit)
    await bot.start(DISCORD_API_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
