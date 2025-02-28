from discord.ext import commands
import yt_dlp

from classes.music import Music
from tasks.queues import music_queue
from enums.operation_modes import ModeManager, OperationMode


class MusicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.curr_msc = None

    def get_music_from_yt(self, query):
        ydl_opts = {
            "quiet": True,
            "noplaylist": True,
            "format": "bestaudio/best",
            "max_downloads": 1,
            "no_warnings": True,
            "simulate": True,
            "noremem": True,
            "skip_download": True,
            "default_search": "ytsearch",
            "force_generic_extractor": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)
            if "entries" in info and info["entries"]:
                return info["entries"][0]

            return None

    @commands.command(description="Play a song from youtube.")
    async def play(self, ctx, query: str):
        if ctx.voice_client is not None:
            if ctx.author.voice is None:
                await ctx.send("You need to be in a voice channel.")
                return

            if ctx.voice_client.channel != ctx.author.voice.channel:
                await ctx.send("You need to be in the same voice channel as the bot.")
                return

        if ModeManager.get_mode() != OperationMode.PLAYBACK:
            await ctx.send("This command is disabled in this operation mode.")
            return

        ydl_info = self.get_music_from_yt(query)
        music = Music(ydl_info, ctx)

        if music is None:
            await ctx.send("No results found.")
            return

        if music_queue.full():
            _ = music_queue.get()

        await music_queue.put(music)
