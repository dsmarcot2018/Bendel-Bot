# code tutorial for starting up the bot was @
# https://realpython.com/how-to-make-a-discord-bot-python/
# bot.py
import os
import random
import getpass
import bendelbucks
import constants
import requests

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

# Initializing BendelBucks class
bb = bendelbucks.BendelBucks()

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


@bot.command(name="bal")
async def bal(ctx):
    await ctx.send(bb.balance(ctx.author.id))


@bot.command(name="hourly")
async def hourly(ctx):
    await ctx.send(bb.add_balance(ctx.author.id, constants.HOURLY_REWARD
                                  , constants.HOURLY_TIMEOUT))


@bot.command(name="daily")
async def daily(ctx):
    await ctx.send(bb.add_balance(ctx.author.id, constants.DAILY_REWARD
                                  , constants.DAILY_TIMEOUT))


@bot.command(name="weekly")
async def weekly(ctx):
    await ctx.send(bb.add_balance(ctx.author.id, constants.WEEKLY_REWARD
                                  ,constants.WEEKLY_TIMEOUT))

# Used for testing
# @bot.command(name="remove")
# async def remove(ctx):
#     await ctx.send(bb.remove_balance(ctx.author.id, 100))


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


@bot.command(name="meme")
async def meme_machine(ctx):
    # The number of images has to be set each time a new image is added.
    num_of_imgs = 38
    # Picks a random number for the image
    ran_pic = random.randint(1, num_of_imgs)
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


bot.run(TOKEN)
