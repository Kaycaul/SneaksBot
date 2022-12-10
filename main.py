import os
import random
import discord
from keep_alive import keep_alive
from discord.ext import commands

reaction_chance = 100

bot = commands.Bot(
	command_prefix="!", # Change to desired prefix
	case_insensitive=True # Commands aren't case-sensitive
)

bot.author_id = 692583640538021908 # Change to your discord id!!!

@bot.event 
async def on_ready(): # When the bot is ready
    print(f"{bot.user} online") # Prints the bot's username and identifier

async def react_random(message: discord.Message):
  # randomly abort like 99% of the time
  if random.randint(0, reaction_chance) != 0:
    return
  # react to the message with a random guild emoji
  emoji = random.choice(message.guild.emojis)
  print(f"Reacting to {message.author}'s message with {emoji.name}")
  if emoji:
    await message.add_reaction(emoji)

async def react_d20(message: discord.Message):
  if " d20 " in message.content:
    await message.add_reaction("<:presence:941828627807490048>")

@bot.event
async def on_message(message: discord.Message):
  if message.author == bot.user:
    return
  react_random(message)

extensions = [
	'cogs.cog_example'  # Same name as it would be if you were importing it
]

if __name__ == '__main__':  # Ensures this is the file being ran
	for extension in extensions:
		bot.load_extension(extension) # Loads every extension.

keep_alive()  # Starts a webserver to be pinged.
token = os.environ.get("DISCORD_BOT_SECRET") 
bot.run(token) # Starts the bot