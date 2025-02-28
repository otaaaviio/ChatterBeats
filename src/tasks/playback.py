import asyncio
import logging
import discord

from tasks.queues import music_queue
from classes.music import Music
from views.playback import PlaybackView


async def process_msc(music: Music):
    try:
        voice_client = music.ctx.voice_client

        if voice_client is None:
            if music.ctx.author.voice:
                voice_client = await music.ctx.author.voice.channel.connect(
                    reconnect=True, timeout=60, self_deaf=True
                )
            else:
                await music.ctx.send("You are not connected to a voice channel.")
                return

        embed = discord.Embed(
            title="Now Playing:",
            description=f"[{music.title}]({music.video_url}) - {music.playtime}",
            color=discord.Color.green(),
        )
        message = await music.ctx.send(
            embed=embed, view=PlaybackView(bot=music.ctx.bot, music=music)
        )

        music_commands = music.ctx.bot.get_cog("MusicCommands")

        if music_commands:
            music_commands.curr_msc = music

        ffmpeg_options = {
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -nostdin",
            "options": "-vn -loglevel panic -bufsize 64k",
        }

        FFMPEG_SOURCE = discord.FFmpegPCMAudio(music.url, **ffmpeg_options)

        voice_client.play(
            FFMPEG_SOURCE,
            after=lambda e: print(f"Erro: {e}") if e else logging.debug("Song ended"),
        )

        while voice_client.is_playing():
            await asyncio.sleep(0.1)

        await message.delete()

    except Exception as e:
        logging.error(e)
        await music.ctx.send(
            "An error occurred while trying to play the song:" + str(e)
        )
    finally:
        music_queue.task_done()
