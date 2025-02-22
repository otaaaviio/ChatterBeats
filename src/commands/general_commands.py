import os
import sys
import discord
from discord.ext import commands, tasks
from enums.languages import available_languages


class GeneralCommands(commands.Cog):
    def __init__(self, bot):
        self.enabled_to_speak_messages = True
        self.current_language = list(available_languages.keys())[0]
        self.bot = bot

    @commands.command(description="Set the language for OtaBot.")
    async def setlang(self, ctx, arg):
        if arg in available_languages.keys():
            self.current_language = arg
            await ctx.send(f"Language set to {self.current_language}")
        else:
            await ctx.send(
                f"Language not available. Type .languages to see all available languages."
            )

    @commands.command(description="Get all available languages for OtaBot.")
    async def languages(self, ctx):
        embed = discord.Embed(
            title="Available languages for OtaBot:",
            description="\n\n".join(
                f"**{key}** → {value}" for key, value in available_languages.items()
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

    @commands.command(description="Leave the voice channel.")
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
            "Speaking": self.enabled_to_speak_messages,
            "Language": available_languages[self.current_language],
            "Channel": ctx.guild.voice_client.channel,
        }
        embed = discord.Embed(
            title="OtaBot status:",
            description="\n\n".join(
                f"**{key}**: {value}" for key, value in msgs.items()
            ),
            color=discord.Color.blue(),
        )
        await ctx.send(embed=embed)

    @commands.command(description="Enable OtaBot to speak messages in chat.")
    async def enable(self, ctx):
        self.enabled_to_speak_messages = True
        await ctx.send(f"OtaBot is now ready to speak messages in chat.")

    @commands.command(description="Disable OtaBot from speaking messages in chat.")
    async def disable(self, ctx):
        self.enabled_to_speak_messages = False
        await ctx.send(f"OtaBot is no longer speaking messages in chat.")

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
