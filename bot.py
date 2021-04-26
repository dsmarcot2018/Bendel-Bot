# code tutorial for starting up the bot was @
# https://realpython.com/how-to-make-a-discord-bot-python/
# bot.py
import os
import random
import getpass
import bendelbucks
import constants
import youtube_dl
import requests
import asyncio
import time


import discord
from dotenv import load_dotenv

from discord.ext import commands

music_queue = []

intents = discord.Intents.default()
intents.members = True

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
# GENERAL_TXT_CHANNEL = os.getenv('DISCORD_GENERAL_CHANNEL_ID')

bot = commands.Bot(command_prefix='!', intents=intents)

# client = discord.Client()

# Initializing BendelBucks class
bb = bendelbucks.BendelBucks()

# bot say's hi once joined
@bot.event
async def send_joined_message():
    channel = bot.get_channel(809191274976247851)
    await channel.send(">>> Bendel-Bot is online! (Brought online by:" +
                       getpass.getuser() + ")\nWhat's up gamers?")


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
    # This is the list containing a tuple holding (role, msg, emoji)
    # for react roles functionality
    bot.reaction_roles = []
    await send_joined_message()


# Welcome message code
@bot.event
async def on_member_join(member):
    print(f"{member.name} Joined the server")
    bb.create_user(member.id)
    # list contains the possible welcome strings and @ mention
    welcome_message_list = [">>> Howdy " + member.mention,
                            ">>> Welcome aboard " + member.mention,
                            ">>> You have entered the gauntlet " + member.mention,
                            ">>> Welcome to the vault " + member.mention,
                            ">>> " + member.mention + "hope you have insurance",
                            ">>> Oh ho ho look at Mr/Ms Cool Guy " + member.mention,
                            ">>> Rip and Tear " + member.mention,
                            ">>> Hide your Bendel-Bucks " + member.mention + " is here",
                            ">>> " + member.mention + " is a Genji main",
                            ">>> " + member.mention + " is a Hanzo main",
                            ">>> " + member.mention + " is a Mercy main",
                            ">>> " + member.mention + " is a Junkrat main"]

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
        await ctx.send(">>> Error enter ints \nuse command  like !roll 2d20")
        return

    i = 0
    roll_result = 0
    while i < int(num_of_dice):
        roll_result += random.randint(1, int(die_sides))
        i += 1
    await ctx.send(">>> Rolling: " + str(num_of_dice) + "d" + str(die_sides) +
                   "\nRolled: " + str(roll_result))

    return


@bot.command(name="bal")
async def bal(ctx):
    await ctx.send('>>> ' + bb.balance(ctx.author.id))


@bot.command(name="hourly")
async def hourly(ctx):
    await ctx.send('>>> ' + bb.add_balance(ctx.author.id, constants.HOURLY_REWARD
                                  , constants.HOURLY_TIMEOUT))


@bot.command(name="daily")
async def daily(ctx):
    await ctx.send('>>> ' + bb.add_balance(ctx.author.id, constants.DAILY_REWARD
                                  , constants.DAILY_TIMEOUT))


@bot.command(name="weekly")
async def weekly(ctx):
    await ctx.send('>>> ' + bb.add_balance(ctx.author.id, constants.WEEKLY_REWARD
                                  ,constants.WEEKLY_TIMEOUT))

# Used for testing
# @bot.command(name="remove")
# async def remove(ctx):
#     await ctx.send(bb.remove_balance(ctx.author.id, 100))


@bot.event
async def on_member_join(member):
    """Bot will send new member server rules."""


# Plays music provided by the user.
# example !play youtube_link vc
# @param youtube_link - A link to a youtube video that you would like
#        to play through the bot.
# @param vc - The voice channel you would like the bot to join.
@bot.command(name="play")
async def play(ctx, url : str):
    music_queue.append(url)
    print(music_queue)
    channel = ctx.author.voice.channel

    voice_channel = discord.utils.get(ctx.guild.voice_channels, name=channel)

    try:
        await channel.connect()
    except discord.errors.ClientException:
        pass

    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        play_next(ctx)
        await ctx.send(">>> Now playing...")
    else:
        await ctx.send('>>> Song queued')


def play_next(ctx):
    vc = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    if len(music_queue) >= 1:
        source = None
        old_download = False
        url_split = music_queue[0].split("=")
        final_split = url_split[1].split("&")
        print(final_split[0])
        for file in os.listdir("./"):
            if file.endswith(final_split[0] + ".mp3"):
                old_download = True

        if not old_download:
            ydl = youtube_dl.YoutubeDL(ydl_opts)
            ydl.download([music_queue[0]])

        for file in os.listdir("./"):
            if file.endswith(final_split[0] + ".mp3"):
                source = file

        del music_queue[0]
        vc.play(discord.FFmpegPCMAudio(source=source), after=lambda e: play_next(ctx))
    else:
        asyncio.run_coroutine_threadsafe(ctx.send(">>> No more songs in queue"), bot.loop)
        time.sleep(30)  # wait 1 minute and 30 seconds
        if not vc.is_playing():
            asyncio.run_coroutine_threadsafe(vc.disconnect(), bot.loop)


@bot.command()
async def dequeue(ctx, num):
    try:
        music_queue.pop(int(num)-1)
        await ctx.send('>>> Song removed from queue')
    except IndexError:
        await ctx.send('>>> There is no song at that queue position')


@bot.command()
async def queue(ctx):
    if len(music_queue) >= 1:
        counter = 1
        for item in music_queue:
            await ctx.send('>>> **' + str(counter) + ':** ' + item + '\n')
            counter += 1
    else:
        await ctx.send('>>> There are no songs in the queue')


@bot.command()
async def skip(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    try:
        voice.stop()
        await ctx.send('>>> Skipped song')
    except AttributeError:
        await ctx.send('>>> There are no songs currently playing')


@bot.command()
async def queue_first(ctx, url : str):
    if bb.remove_balance(ctx.author.id, 100)[:7] == "Removed":
        await play(ctx, url)
        music_queue.insert(0, music_queue.pop())
    else:
        await ctx.send('>>> ' + bb.remove_balance(ctx.author.id, 100))


# Leaves the voice channel it is connected to.
# Only leaves if it is connected and will send an error message if not.
@bot.command()
async def leave(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    music_queue.clear()
    try:
        await voice.disconnect()
    except AttributeError:
        await ctx.send(">>> Bot is not connected to a voice channel")


# Pauses the audio that is currently playing.
# Only pauses if it is connected and playing and will send an error message if not.
@bot.command()
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    try:
        voice.pause()
        await ctx.send(">>> Music paused")
    except AttributeError:
        await ctx.send(">>> Bot cannot be paused at this moment")


# Resumes paused audio.
# Only resumes if it is connected and paused and will send an error message if not.
@bot.command()
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    try:
        voice.resume()
        await ctx.send(">>> Music resumed")
    except AttributeError:
        await ctx.send(">>> Bot cannot be resumed at this moment")


# Stops the audio.
# Only stops if it is connected and will send an error message if not.
@bot.command()
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    music_queue.clear()

    try:
        voice.stop()
        await ctx.send(">>> Music stopped")
    except AttributeError:
        await ctx.send(">>> Bot cannot be stopped at this moment")
        

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
        await ctx.send(">>> Invalid Arguments")


previous_images = []
@bot.command(name="meme")
async def meme_machine(ctx):
    # The number of images has to be set each time a new image is added.
    num_of_imgs = 46
    # Picks a random number for the image
    while True:
        repeate = False
        ran_pic = random.randint(1, num_of_imgs)
        for prev in previous_images:
            if ran_pic == prev:
                repeate = True
        if not repeate:
            break
    # Sets previous_image to last image so it isn't repeted.
    if len(previous_images) == 5:
        del previous_images[0]
        previous_images.append(ran_pic)
    else:
        previous_images.append(ran_pic)
    # This links to our github to retrieve the image
    link = 'https://raw.githubusercontent.com/dsmarcot2018/Bendel-Bot/main/memes/' + str(ran_pic) + '.png'
    # Checks to see if the image can be resolved, If not it will try again with the extension .jpg instead of .png
    request = requests.get(link)
    if request.status_code == 404:
        link = 'https://raw.githubusercontent.com/dsmarcot2018/Bendel-Bot/main/memes/' + str(ran_pic) + '.jpg'
        request = requests.get(link)

    if request.status_code == 404:
        await ctx.send("Could not resolve image: " + str(ran_pic))
    else:
        await ctx.send(link)


@bot.command(name="dogo")
async def dogo_machine(ctx):
    # URL to get random dog images
    url = "https://dog.ceo/api/breeds/image/random"
    r = requests.get(url)
    # parsing Json
    url_to_parse = r.json()
    url_parsed = str(url_to_parse).split("'")
    url = url_parsed[3]
    await ctx.send(url)


bot.run(TOKEN)
