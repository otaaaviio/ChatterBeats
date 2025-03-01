import discord
from tasks.queues import music_queue


class PlaybackView(discord.ui.View):
    def __init__(self, *, bot, music):
        super().__init__()
        self.bot = bot
        self.curr_msc = music

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

    @discord.ui.button(emoji="📘", style=discord.ButtonStyle.gray)
    async def button_queue(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await list_queue(interaction)


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


async def list_queue(interaction: discord.Interaction, curr_msc):
    queue = []

    if curr_msc:
        queue.append(curr_msc)

    for _ in range(music_queue.qsize()):
        song = await music_queue.get()
        queue.append(song)
        await music_queue.put(song)

    if not queue:
        await interaction.response.send_message("The queue is empty.", ephemeral=True)
        return

    embed = discord.Embed(
        title="Queue:",
        description="\n".join(
            [f"{i + 1}. [{msc.title}]({msc.url})" for i, msc in enumerate(queue)]
        ),
        color=discord.Color.green(),
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)
