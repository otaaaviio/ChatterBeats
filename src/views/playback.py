import discord
from tasks.queues import music_queue


class PlaybackView(discord.ui.View):
    def __init__(self, *, bot):
        super().__init__()
        self.bot = bot

    @discord.ui.button(emoji="⏯️", style=discord.ButtonStyle.gray)
    async def button_resume_or_pause(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await resume_or_pause(interaction)

    @discord.ui.button(emoji="⏭️", style=discord.ButtonStyle.gray)
    async def button_skip(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await skip(interaction)

    @discord.ui.button(emoji="⏹️", style=discord.ButtonStyle.gray)
    async def button_stop(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await stop(interaction)

    @discord.ui.button(emoji="📘", style=discord.ButtonStyle.gray)
    async def button_queue(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await list_queue(interaction)

    @discord.ui.button(emoji="🔁", style=discord.ButtonStyle.gray)
    async def button_autoplay(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await autoplay(interaction)


async def resume_or_pause(interaction: discord.Interaction):
    if interaction.guild.voice_client:
        if interaction.guild.voice_client.is_playing():
            interaction.guild.voice_client.pause()
            await interaction.response.send_message("Music paused.", ephemeral=True)
        elif interaction.guild.voice_client.is_paused():
            interaction.guild.voice_client.resume()
            await interaction.response.send_message("Music resumed.", ephemeral=True)
        else:
            await interaction.response.send_message(
                "I'm not playing anything.", ephemeral=True
            )


async def skip(interaction: discord.Interaction):
    if interaction.guild.voice_client:
        if interaction.guild.voice_client.is_playing():
            interaction.guild.voice_client.stop()
            await interaction.response.send_message("Music skipped.", ephemeral=True)
        else:
            await interaction.response.send_message(
                "I'm not playing anything.", ephemeral=True
            )


async def stop(interaction: discord.Interaction):
    if interaction.guild.voice_client:
        if interaction.guild.voice_client.is_playing():
            interaction.guild.voice_client.stop()
            await interaction.response.send_message("Music stopped.", ephemeral=True)
        else:
            await interaction.response.send_message(
                "I'm not playing anything.", ephemeral=True
            )


async def list_queue(interaction: discord.Interaction):
    if music_queue.empty():
        await interaction.response.send_message("The queue is empty.", ephemeral=True)
    else:
        queue = []
        for i in range(music_queue.qsize()):
            queue.append(await music_queue.get())
        await interaction.response.send_message(queue, ephemeral=True)
        for i in range(len(queue)):
            await music_queue.put(queue[i])


async def autoplay(interaction: discord.Interaction):
    pass
