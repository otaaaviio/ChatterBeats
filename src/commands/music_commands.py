import discord
from discord.ext import commands
import yt_dlp

from classes.music import Music
from tasks.queues import music_queue
from enums.operation_modes import OperationMode


class MusicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_related_music(self, video_id):
        ydl_opts = {
            "quiet": True,
            "format": "bestaudio",
            "noplaylist": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(
                f"https://www.youtube.com/watch?v={video_id}", download=False
            )
            if "related_videos" in info:
                for related in info["related_videos"]:
                    if "id" in related:
                        related_info = self.get_music_from_yt(related["id"])
                        if related_info:
                            return related_info
        return None

    def get_music_from_yt(self, query):
        ydl_opts = {
            "quiet": True,
            "noplaylist": True,
            "format": "bestaudio",
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

        op_mode = self.bot.get_cog("GeneralCommands").op_mode

        if op_mode != OperationMode.PLAYBACK:
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

    # @commands.command()
    # async def autoplay(self, ctx):
    #     self.autoplay = not self.autoplay
    #     await ctx.send(f"Autoplay is now {'enabled' if self.autoplay else 'disabled'}.")

    #     while not music_queue.full():
    #         msc_info = self.get_related_music(self.curr_msc.id)
    #         if msc_info:
    #             music = Music(msc_info, ctx)
    #             print(music)
    #             await music_queue.put(music)
    #         else:
    #             break
