import asyncio
import datetime
import logging
import discord
from discord.ext import commands
import yt_dlp

def search_youtube(query):
    ydl_opts = {
        'quiet': True,
        "noplaylist": True,
        'format': 'bestaudio',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)
        if 'entries' in info and info['entries']:
            return info['entries'][0]['url']
        
        return None

class MusicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Play a song from youtube.")
    async def play(self, ctx, query: str):
        try:
            if not ctx.voice_client:
                if ctx.author.voice:
                    await ctx.author.voice.channel.connect()
                else:
                    await ctx.send("You are not connected to a voice channel.")
                    return

            ffmpeg_options = {
                "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
                "options": "-vn"
            }

            url = search_youtube(query)
            if not url:
                await ctx.send("No results found.")
                return
            
            voice_client = ctx.voice_client
            voice_client.stop()
            FFMPEG_SOURCE = discord.FFmpegPCMAudio(url, **ffmpeg_options)

            voice_client.play(FFMPEG_SOURCE, after=lambda e: print(f"Erro: {e}") if e else None)
            
            while voice_client.is_playing():
                await asyncio.sleep(1)

        except Exception as e:
            logging.error(e)
            await ctx.send("An error occurred while trying to play the song: " + str(e))

    @commands.command()
    async def stop(self, ctx):
        if ctx.voice_client:
            if ctx.voice_client.is_playing():
                ctx.voice_client.stop()
                await ctx.send("Stopped.")
            else:
                await ctx.send("I'm not playing anything.")