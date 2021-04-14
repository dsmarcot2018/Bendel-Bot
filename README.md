# Bendel-Bot
## Authors

* Raymond Zheng
* Hunter Spack
* Drew Marcotte
* Joe Marchesini

## Pip Installs

In the command line you must run each of these pip installs for all the required packages:

1. "pip install -U discord.py"
2. "pip install -U python-dotenv"
3. "pip install -U requests"
4. "pip install --upgrade youtuble-dl"
5. "pip install PyNaCl"

## Bot Set Up

1. Open the bot folder as a project in PyCharm and then set up a virtual environment for your bot.
2. Create a .env file with a token provided by one of the developers and put this text in it in this format: DISCORD_TOKEN=PROVIDED_TOKEN
3. Navigate to the folder containing the bot in your command line.
4. Run the command "python bot.py" in your command line to run the bot.

If you are just running the bot on your computer, terminate using the Control key and C hotkey, otherwise terminate like you would any other program.

## Features
**Welcome Messages**
- Bendel-Bot gives new server members a warm welcome with any one of 15+ welcome messages

**Music**
- Plays music through the bot using youtube-dl
- Commands
  - !play youtube-link vc
    - @param youtube-link - A link to the youtube video that you would like to play.
    - @param vc - The exact name of the vc you would like the bot to join.
    - Plays a youtube link's audio through the bot.
  - !pause
    - Pauses the audio.
  - !resume
    - Resumes paused audio.
  - !stop
    - Stops the audio, but leaves the bot in the channel.
  - !leave
    - Leaves the vc and stops the audio.

**Currency System**
- Use !hourly, !daily, !weekly to claim rewards.

**React Roles**
- React to a message with an emoji to assign yourself a role.
- Use !roleset (Role Name) (msg id to react to) (Emoji) to configure.
- Ex. !roleset dev 824395559791755374 :thumbsup:

**Meme Machine**
- You can run the command !meme in chat and you will get a random image back from out github

## Planned Bot Features
**Meme Delivery**
- Bendel-Bot will share a random meme on command from their personal stash 

**Future Currency Features**
- !bal to see BBs
- Members will be able to spend Bendel-Bucks on a number of different activities

**Slot Machine**
- One of those planned activities is Bendel-Bot's slot machine where server members will be able to spend BBs to give it a spin to try and win more BBs

**Music**
- Adding a queuing feature.
- Removing the vc param for !play and making the bot join the vc of the user who used the command.

## Features that are less certain to be featured
**Bendel-Buck Leaderboard**
- Run a command to see the top Bendel-Buck earners on the server
