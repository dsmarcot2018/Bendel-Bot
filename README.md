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
4. "pip install --upgrade youtube-dl"
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
  - !play youtube-link
    - @param youtube-link - A link to the youtube video that you would like to play.
    - Plays a youtube link's audio through the bot.
    - Queues the song if one is already playing.
  - !pause
    - Pauses the audio.
  - !resume
    - Resumes paused audio.
  - !stop
    - Stops the audio, but leaves the bot in the channel.
  - !leave
    - Leaves the vc and stops the audio.
  - !queue
    - Lists out the currently queued songs.
  - !dequeue song-position
    - @param song-position - The position in the queue of the song you would like to remove.
    - Removes a song from the queue.
  - !skip
    - Skips the currently playing song.
  - !queue_first youtube-link
    - @param youtube-link - A link to the youtube video that you would like to play.
    - Costs 100 Bendel-Bucks to use this function.
    - Puts the requested song at the front of the queue.

**Currency System**
- Use !hourly, !daily, !weekly to claim rewards.
- Use !bal to check balance.

**Slot Machine**
- Bendel-Bot's slot machine where server members will be able to spend BBs to give it a spin to try and win more BBs.
- !slot bet-money
  - @param bet-money - The amount of BBs you would like to bet at the slot machine.
  - Rolls 3 random slots and if they all match the user wins back extra BB's

**React Roles**
- React to a message with an emoji to assign yourself a role.
- Use !roleset (Role Name) (msg id to react to) (Emoji) to configure.
- Ex. !roleset dev 824395559791755374 :thumbsup:

**Meme Machine**
- You can run the command !meme in chat and you will get a random image back from out github, it holds the last 5 memes so they don't repeat.

**Dogo Machine**
- You can run the command !dogo in chat and you will get a random dog image from an online api.

## Planned Bot Features
**Future Currency Features**
- Members will be able to spend Bendel-Bucks on a number of different activities.

**Music**
- Making it so only the user that requested a song can dequeue it or the one that would like to dequeue it must pay some BBs.

## Features that are less certain to be featured
**Bendel-Buck Leaderboard**
- Run a command to see the top Bendel-Buck earners on the server.
