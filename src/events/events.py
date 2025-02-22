import asyncio
import logging
import os
import discord
from dotenv import load_dotenv
from enums.errors import Error
from tasks.voice_channel import message_queue

load_dotenv()
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")


def setup_events(bot, general_commands):
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

        if type(exception) in Error.get_allowed_errors():
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
