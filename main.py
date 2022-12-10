import os
import random
import discord
from keep_alive import keep_alive
from discord.ext import commands

class SneaksMemory:
  last_four_messages = []

memory = SneaksMemory()

reaction_chance = 99
# dictionary of emotes and their ids
emotes = {
  "presence" : "<:presence:941828627807490048>",
  "bl" : "<:bl:996875747346100354>"
}
# dictionary of what emotes to use to react to which messages
keyword_reactions = {
  "d20" : "presence",
  "sneaks" : "bl"
}

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
  if not isinstance(message.channel, discord.DMChannel):
    # select a random guild emoji
    emoji = random.choice(message.guild.emojis)
  else:
    emoji = emotes[random.choice(emotes.keys())]
  # react with the emoji if you find it
  if emoji:
    print(f"Reacting to {message.author}: \"{message.content}\" with {emoji}")
    await message.add_reaction(emoji)

async def react_keywords(message: discord.Message):
  # react to keywords
  for keyword in keyword_reactions.keys():
    # if the key is in the message
    if keyword in message.content.lower():
      # react with the value of the key
      print(f"Reacting to {message.author}: \"{message.content}\" with {emotes[keyword_reactions[keyword]]}")
      await message.add_reaction(emotes[keyword_reactions[keyword]])

async def chain_message(message: discord.Message):
  # save the last 4 messages received
  memory.last_four_messages.insert(0, message.content)
  if len(memory.last_four_messages) > 4:
    memory.last_four_messages.pop()
  else:
    return
  # check if memory is repetitve 
  for v in memory.last_four_messages[1:]:
    if v != memory.last_four_messages[0]:
      return
  # contribute to the spam
  print(f"Spamming {message.content}")
  await message.reply(
    content=message.content,
    reference=message.to_reference(),
    mention_author=True
    )
  # clear memory
  memory.last_four_messages = []
  

@bot.event
async def on_message(message: discord.Message):
  if message.author == bot.user:
    return
  await react_random(message)
  await react_keywords(message)
  await chain_message(message)

extensions = [
	'cogs.cog_example'  # Same name as it would be if you were importing it
]

if __name__ == '__main__':  # Ensures this is the file being ran
	for extension in extensions:
		bot.load_extension(extension) # Loads every extension.

keep_alive()  # Starts a webserver to be pinged.
token = os.environ.get("DISCORD_BOT_SECRET") 
bot.run(token) # Starts the bot