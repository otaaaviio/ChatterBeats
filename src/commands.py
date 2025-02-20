import discord
from discord.ext import commands, tasks
from enums.languages import available_languages


class BotCommands(commands.Cog):
    def __init__(self, bot):
        self.enabled_to_speak_messages = False
        self.current_language = list(available_languages.keys())[0]
        self.bot = bot

    @commands.command(name="set-lang")
    async def set_lang(self, ctx, arg):
        if arg in available_languages.keys():
            self.current_language = arg
            await ctx.send(f"Language set to {self.current_language}")
        else:
            await ctx.send(
                f"Language not available. Type .languages to see all available languages."
            )

    @commands.command()
    async def languages(self, ctx):
        embed = discord.Embed(
            title="Available languages for OtaBot:",
            description="\n\n".join(
                f"**{key}** → {value}" for key, value in available_languages.items()
            ),
            color=discord.Color.blue(),
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
            await ctx.send(f"Joined {channel}.")
        else:
            await ctx.send(f"You need to be in a voice channel to use this command.")

    @commands.command()
    async def leave(self, ctx):
        if ctx.guild.voice_client:
            await ctx.guild.voice_client.disconnect()
            await ctx.send(f"Left voice channel.")
        else:
            await ctx.send(f"OtaBot is not in a voice channel.")

    @commands.command()
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

    @commands.command()
    async def enable(self, ctx):
        self.enabled_to_speak_messages = True
        await ctx.send(f"OtaBot is now ready to speak messages in chat.")

    @commands.command()
    async def disable(self, ctx):
        self.enabled_to_speak_messages = False
        await ctx.send(f"OtaBot is no longer speaking messages in chat.")

    @commands.command()
    async def otabot(self, ctx):
        embed = discord.Embed(
            title="Hello!",
            description="I am OtaBot, a bot created by @ota_targaryen.\n\n I can join your voice channel and speak messages in chat.\n\n Type .help to see all available commands.",
            color=discord.Color.blue(),
        )
        await ctx.send(embed=embed)

    @tasks.loop(seconds=10)
    async def check_speak_status(self):
        if self.enabled_to_speak_messages:
            print(f"OtaBot is enabled to speak messages.")

        else:
            print(f"OtaBot is not enabled to speak messages.")

    @check_speak_status.before_loop
    async def before_check_speak_status(self):
        await self.bot.wait_until_ready()
