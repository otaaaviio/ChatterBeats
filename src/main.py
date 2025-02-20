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


def main():
    DISCORD_API_TOKEN = os.getenv("DISCORD_API_TOKEN")
    bot.run(DISCORD_API_TOKEN)


if __name__ == "__main__":
    main()
