# code tutorial for starting up the bot was @
# https://realpython.com/how-to-make-a-discord-bot-python/
# bot.py
import os
import random
import getpass
import youtube_dl

import discord
from dotenv import load_dotenv

from discord.ext import commands


intents = discord.Intents.default()
intents.members = True

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
# GENERAL_TXT_CHANNEL = os.getenv('DISCORD_GENERAL_CHANNEL_ID')

bot = commands.Bot(command_prefix='!', intents=intents)

# client = discord.Client()


# bot say's hi once joined
@bot.event
async def send_joined_message():
    channel = bot.get_channel(809191274976247851)
    await channel.send("Bendel-Bot is online! (Brought online by:" +
                       getpass.getuser() + ")")
    await channel.send("What's up gamers?")


@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
        f'{bot.user.name} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')
    await send_joined_message()


# Welcome message code
@bot.event
async def on_member_join(member):
    print(f"{member.name} Joined the server")

    # list contains the possible welcome strings and @ mention
    welcome_message_list = ["Howdy " + member.mention,
                            "Welcome aboard " + member.mention,
                            "You have entered the gauntlet " + member.mention,
                            "Welcome to the vault " + member.mention,
                            member.mention + "hope you have insurance",
                            "Oh ho ho look at Mr/Ms Cool Guy " + member.mention,
                            "Rip and Tear " + member.mention,
                            "Hide your Bendel-Bucks " + member.mention + " is here",
                            member.mention + " is a Genji main",
                            member.mention + " is a Hanzo main",
                            member.mention + " is a Mercy main",
                            member.mention + " is a Junkrat main"]

    # sets the channel to the welcome (general) channel
    channel = bot.get_channel(809191274976247851)

    # sets the message to one of the choices
    response = random.choice(welcome_message_list)
    await channel.send(response)


@bot.command(name="Welcome")
async def welcome(ctx):
    print(f"welcome heard")

    # old/
    # if message.author == client.user:
    #    return
    # if message.content == '!Welcome':
    #   response = "Howdy"
    # await message.channel.send(response)
    # elif message.content == 'raise-exception':
    # raise discord.DiscordException
    # old/

    response = f"Howdy {ctx.author}"
    await ctx.send(response)


@bot.command()
async def play(ctx, url : str, channel):
    """Code heavily based off of code done in this youtube video https://www.youtube.com/watch?v=ml-5tXRmmFk"""
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current song to end or use the stop command")
        return

    voice_channel = discord.utils.get(ctx.guild.voice_channels, name=channel)
    await voice_channel.connect()

    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'prefferedcodec': 'mp3',
            'prefferedquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))


@bot.command()
async def leave(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("Bot is not connected to a voice channel.")


@bot.command()
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Bot is not playing.")


@bot.command()
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.sent("Audio is not paused")


@bot.command()
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.stop()

bot.run(TOKEN)