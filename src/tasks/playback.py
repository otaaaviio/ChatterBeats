import asyncio
import logging
import discord

from tasks.queues import music_queue
from classes.music import Music
from views.playback import PlaybackView


async def process_msc(music: Music):
    try:
        embed = discord.Embed(
            title="Now Playing:",
            description=f"[{music.title}]({music.video_url}) - {music.playtime}",
            color=discord.Color.green(),
        )
        await music.ctx.send(
            embed=embed, view=PlaybackView(bot=music.ctx.bot, music=music)
        )

        ffmpeg_options = {
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
            "options": "-vn",
        }
        music_commands = music.ctx.bot.get_cog("MusicCommands")

        if music_commands:
            music_commands.curr_msc = music

        voice_client = music.ctx.voice_client
        url = music.url
        FFMPEG_SOURCE = discord.FFmpegPCMAudio(url, **ffmpeg_options)

        if voice_client is None:
            if music.ctx.author.voice:
                voice_client = await music.ctx.author.voice.channel.connect(
                    reconnect=True, timeout=60, self_deaf=True
                )
            else:
                await music.ctx.send("You are not connected to a voice channel.")
                return

        voice_client.play(
            FFMPEG_SOURCE,
            after=lambda e: print(f"Erro: {e}") if e else logging.debug("Song ended"),
        )

        while voice_client.is_playing():
            await asyncio.sleep(1)

    except Exception as e:
        logging.error(e)
        await music.ctx.send(
            "An error occurred while trying to play the song:" + str(e)
        )
    finally:
        music_queue.task_done()
