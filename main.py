import os
import discord
from keep_alive import keep_alive
from sneaks import Sneaks
print(f"running discord api {discord.__version__}")

# create a new sneaksbot
sneaksbot = Sneaks()
bot = sneaksbot.bot

@bot.event
async def on_ready():  # When the bot is ready
    print(f"{bot.user} online\nLoggers!!")  # Prints the bot's username and identifier 
    # begin all the infinitely looping coroutines
    await sneaksbot.update_active_role(30)
    await sneaksbot.update_status(5) # this will recur every 10 minutes


@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return
    await sneaksbot.react_random(message)
    await sneaksbot.react_keywords(message)
    await sneaksbot.chain_message(message)
    await sneaksbot.reply_ping(message)

extensions = [
    'cogs.cog_example'  # Same name as it would be if you were importing it
]

if __name__ == '__main__':  # Ensures this is the file being ran
    for extension in extensions:
        bot.load_extension(extension)  # Loads every extension.

keep_alive()  # Starts a webserver to be pinged.
token = os.environ.get("DISCORD_BOT_SECRET")
bot.run(token)  # Starts the bot