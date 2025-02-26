import os
import sys
import discord
from discord.ext import commands
from enums.languages import Language, LanguageManager
from enums.operation_modes import ModeManager, OperationMode


class GeneralCommands(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.command(description="Set the language for OtaBot.")
    async def setlang(self, ctx, lang):
        if lang in Language.get_available_languages():
            LanguageManager.set_language(lang)
            await ctx.send(f"Language set to {Language.get_fullname_language(lang)}")
        else:
            await ctx.send(
                f"Language not available. Type .languages to see all available languages."
            )

    @commands.command(description="Get all available languages for OtaBot.")
    async def languages(self, ctx):
        embed = discord.Embed(
            title="Available languages for OtaBot:",
            description="\n".join(
                f"**{value}**: {key}" for key, value in Language.get_all_languages()
            ),
            color=discord.Color.blue(),
        )
        await ctx.send(embed=embed)

    @commands.command(description="Join the voice channel.")
    async def join(self, ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel

            await channel.connect(self_deaf=True)
            await ctx.send(f"Joined {channel}.")
        else:
            await ctx.send(f"You need to be in a voice channel to use this command.")

    @commands.command(description="Leave the voice channel.", title="Leave")
    async def leave(self, ctx):
        if ctx.guild.voice_client:
            await ctx.guild.voice_client.disconnect()
            await ctx.send(f"Left voice channel.")
        else:
            await ctx.send(f"OtaBot is not in a voice channel.")

    @commands.command(
        description="Get the current status of OtaBot, like language, channel and if it is enabled to speak messages."
    )
    async def status(self, ctx):
        msgs = {
            "Mode": OperationMode.get_description_mode(ModeManager.get_mode().value),
            "Language": Language.get_fullname_language(LanguageManager.get_language().value),
            "Channel": (
                ctx.guild.voice_client.channel if ctx.guild.voice_client else "None"
            ),
        }
        embed = discord.Embed(
            title="OtaBot status:",
            description="\n\n".join(
                f"**{key}**: {value}" for key, value in msgs.items()
            ),
            color=discord.Color.blue(),
        )
        await ctx.send(embed=embed)

    @commands.command(
        description="Set the mode for OtaBot. Type .modes to see all available modes."
    )
    async def setop(self, ctx, mode):
        if mode == ModeManager.get_mode().value:
            await ctx.send(
                f"Mode is already set to {OperationMode.get_description_mode(mode)}."
            )
            return

        if mode in OperationMode.get_available_modes():
            ModeManager.set_mode(mode)
            await ctx.send(f"Mode set to {OperationMode.get_description_mode(mode)}.")
            return

        await ctx.send(f"Mode not available. Type .modes to see all available modes.")

    @commands.command(description="Get all available modes for OtaBot.")
    async def modes(self, ctx):
        embed = discord.Embed(
            title="Available modes for OtaBot:",
            description="\n".join(
                f"**{value}**: {key}" for key, value in OperationMode.get_all_modes()
            ),
            color=discord.Color.blue(),
        )
        await ctx.send(embed=embed)

    @commands.command(description="Get to know OtaBot.")
    async def otabot(self, ctx):
        embed = discord.Embed(
            title="Hello!",
            description="I am OtaBot, a bot created by @ota_targaryen.\n\n I can join your voice channel and speak messages in chat.\n\n Type .help to see all available commands.",
            color=discord.Color.blue(),
        )
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def reset(self, ctx):
        if ctx.author.name != "ota_targaryen":
            ctx.send("You don't have permission to use this command.")
            return

        if self.bot.voice_clients:
            for vc in self.bot.voice_clients:
                await vc.disconnect()

        main_path = os.path.join(os.path.dirname(__file__), "..", "main.py")
        main_path = os.path.abspath(main_path)
        os.execv(sys.executable, [sys.executable, main_path])
