# code tutorial for starting up the bot was @
# https://realpython.com/how-to-make-a-discord-bot-python/
# bot.py
import os
import random
import getpass
import constants
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
    for guild in bot.guilds:
        if guild.name == GUILD:
            break
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


@bot.command(name="roll")
async def roll(ctx, die: str):
    try:
        num_of_dice, die_sides = die.split("d")
        print(num_of_dice)
        print(die_sides)
        int(num_of_dice)
        int(die_sides)
    except ValueError:
        await ctx.send("Error enter ints \nuse command  like !roll 2d20")
        return

    i = 0
    while i < int(num_of_dice):
        roll_result = str(random.randint(1, int(die_sides)))
        i += 1
        await ctx.send("Rolling: d" + str(die_sides) +
                       "\nRolled: " + str(roll_result))

    return


# Plays music provided by the user.
# example !play youtube_link vc
# @param youtube_link - A link to a youtube video that you would like
#        to play through the bot.
# @param vc - The voice channel you would like the bot to join.
@bot.command()
async def play(ctx, url : str, channel):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return

    voice_channel = discord.utils.get(ctx.guild.voice_channels, name=channel)

    try:
        await voice_channel.connect()
    except discord.errors.ClientException:
        pass

    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    ydl = youtube_dl.YoutubeDL(ydl_opts)
    ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source="song.mp3"))


# Leaves the voice channel it is connected to.
# Only leaves if it is connected and will send an error message if not.
@bot.command()
async def leave(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    try:
        await voice.disconnect()
    except AttributeError:
        await ctx.send("Bot is not connected to a voice channel.")


# Pauses the audio that is currently playing.
# Only pauses if it is connected and playing and will send an error message if not.
@bot.command()
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    try:
        voice.pause()
    except AttributeError:
        await ctx.send("Bot cannot be paused at this moment.")


# Resumes paused audio.
# Only resumes if it is connected and paused and will send an error message if not.
@bot.command()
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    try:
        voice.resume()
    except AttributeError:
        await ctx.send("Bot cannot be resumed at this moment.")


# Stops the audio.
# Only stops if it is connected and will send an error message if not.
@bot.command()
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    try:
        voice.stop()
    except AttributeError:
        await ctx.send("Bot cannot be stopped at this moment.")
        

@bot.event
async def on_raw_reaction_add(payload):
    """Add role on reaction to message."""

    # Loop through list of tuple to make sure msg_id and emoji name match
    for role, msg, emoji in bot.reaction_roles:
        if msg.id == payload.message_id and emoji == payload.emoji.name:
            # Api call to add role
            await payload.member.add_roles(role)


@bot.event
async def on_raw_reaction_remove(payload):
    """Remove role on remove reaction to message."""

    # Loop through list of tuple to make sure msg_id and emoji name match
    for role, msg, emoji in bot.reaction_roles:
        if msg.id == payload.message_id and emoji == payload.emoji.name:
            # Api call to remove role
            await bot.get_guild(payload.guild_id). \
                get_member(payload.user_id). \
                remove_roles(role)


@bot.command(name="roleset")
async def role_set(ctx, role: discord.Role = None,
                   msg: discord.Message = None,
                   emoji=None):
    """The command used in Discord to configure which message is the target.

    Usage: !roleset (Role Name) (msg id to react to) (Emoji)"""

    # Error handling for command
    if role is not None and msg is not None and emoji is not None:
        await msg.add_reaction(emoji)
        # Appending to the tuple in on_ready()
        bot.reaction_roles.append((role, msg, emoji))
    else:
        await ctx.send("Invalid Arguments")

        
bot.run(TOKEN)
