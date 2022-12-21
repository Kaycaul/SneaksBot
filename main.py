import os
import discord
import asyncio
from keep_alive import keep_alive
from sneaks import Sneaks
print(f"running discord api {discord.__version__}")

# create a new sneaksbot
sneaksbot = Sneaks()
bot = sneaksbot.bot

@bot.event
async def on_ready():  # When the bot is ready
    print(f"\033[1;93m{bot.user} online\nLoggers!!")  # Prints the bot's username and identifier 
    await sneaksbot.update_known_emotes()
    # begin all the infinitely looping coroutines, execute them once per second
    while True:
        await sneaksbot.update_active_role(3600) # this will recur every hour
        await sneaksbot.update_status(600) # this will recur every 10 minutes
        await asyncio.sleep(1)


@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return
    await sneaksbot.react_random(message)
    await sneaksbot.react_keywords(message)
    await sneaksbot.chain_message(message)
    await sneaksbot.reply_ping(message)
    await sneaksbot.emote_dump(message) # this was a mistake

keep_alive()  # Starts a webserver to be pinged.
token = os.environ.get("DISCORD_BOT_SECRET")
bot.run(token)  # Starts the bot