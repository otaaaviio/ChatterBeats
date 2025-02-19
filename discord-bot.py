import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()

DISCORD_API_TOKEN = os.getenv("DISCORD_API_TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

guild = discord.Guild

speak_messages = False

@bot.event
async def on_ready():
    print('bot working: {0.user}'.format(bot))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="!otabot"))

@bot.event
async def on_message(message):
    global speak_messages
    
    if message.author == bot.user:
        return
    
    message_content = message.content
    message_author = message.author
    
    print(f'New message -> {message_author}: {message_content}')
    
    if message_content == "!otabot":
        embed = discord.Embed(
            title = "Hello!",
            description = "I am OtaBot, a bot created by @ota_targaryen. I can join your voice channel and speak messages in chat. Type !help to see all available commands.",
            color = discord.Color.blue()
        )
        await message.channel.send(embed=embed)
    
    if message_content == "!help":
        embed = discord.Embed(
            title = "Commands",
            description = "Here are all the commands you can use with OtaBot: \n\n!join - Join the voice channel\n!leave - Leave the voice channel\n!status - Show the current status of the bot\n!speak-on - Enable the bot to speak messages in chat\n!speak-off - Disable the bot to speak messages in chat",
            color = discord.Color.blue()
        )
        await message.channel.send(embed=embed)

    if message_content == "!join" and message.author.voice:
        channel = message.author.voice.channel
        await channel.connect()
        await message.channel.send(f'Joined {channel}!')
    elif message_content == "!leave" and message.guild.voice_client:
        await message.guild.voice_client.disconnect()
    elif message_content == "!leave" and not message.guild.voice_client:
        await message.channel.send(f'OtaBot is not in a voice channel.')
        
    if message_content == "!status":
        await message.channel.send(f'Spaeking messages: {speak_messages}')
        
    if message_content == "!speak-on":
        speak_messages = True
        await message.channel.send(f'OtaBot is now ready to speak messages in chat.')
        return
        
    if speak_messages:
        if message_content == "!speak-off":
            speak_messages = False
            await message.channel.send(f'OtaBot is no longer speaking messages in chat.')
            return

        text_to_say = message_content
        voice_channel = message.author.voice.channel
        bot_voice_channel = message.guild.voice_client
        
        if bot_voice_channel:
            if voice_channel != bot_voice_channel.channel:
                await message.channel.send(f'OtaBot is already in a voice channel: {bot_voice_channel.channel}')
            else:
                tts_audio_path = "tts_audio.mp3"
                
                os.system(f"gtts-cli '{text_to_say}' --lang pt --output {tts_audio_path}")
                
                bot_voice_channel.play(discord.FFmpegPCMAudio(tts_audio_path), after=lambda e: print('Audio finished'))
                
                while bot_voice_channel.is_playing():
                    await asyncio.sleep(1)
                    
                os.remove(tts_audio_path)

if __name__ == "__main__":
    bot.run(DISCORD_API_TOKEN)