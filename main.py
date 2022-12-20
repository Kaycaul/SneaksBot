import asyncio
import os
import random
import discord
print(f"running discord api {discord.__version__}")
from keep_alive import keep_alive
from discord.ext import commands

class SneaksMemory:
  last_four_messages = []

memory = SneaksMemory()

reaction_chance = 99
update_frequency = 30 # delay in seconds between updates after on_ready
greeting_reactions = ["bl", "boil", "hard", "matt", "sack"]

# list of activities sneaks could be playing, randomly cycled through
activities_playing = [
  "Factorio",
  "Nier Automata",
  "Liquid Skies Zero",
  "with Discord API",
  "Minecraft",
  "Team Fortress Two",
  "plr_hightower",
  "ctf_2fort",
  "Garry's Mod",
  "Half-Life 2",
  "gm_construct",
  "Satisfactory",
  "Beat Saber",
  "Receiver 2",
  "Heat Signature",
  "OpenTTD",
  "Opus Magnum",
  "Krunker",
  "The Witness",
  "Baba Is You",
  "Portal 2",
  "OneShot",
  "Celeste",
  "Spacechem",
  "Terraria",
  "Lego Star Wars",
  "Visual Studio Code",
  "Godot",
  "Github",
  "Replit",
  "Unity Editor",
  "Scratch",
  "Krita"
]

# dictionary of emotes and their ids
emotes = {
  "presence" : "<:presence:941828627807490048>",
  "bl" : "<:bl:996875747346100354>",
  # "gloghi" : "<a:gloghi:1038322477161513021>", # average californian hangout emote
  "boil" : "<a:boil:1045540000600698980>",
  "hard" : "<:hard:924072022777167912>",
  "fuckyou" : "<a:fuckyou:1045005787451375687>",
  "matt" : "<:matt:1031681843600293949>",
  "sack" : "<:sack:924512985504960552>"
}

# dictionary of what emotes to use to react to which messages
keyword_reactions = {
  "d20" : ["presence", "fuckyou"],
  "sneak" : greeting_reactions,
}

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.presences = True
bot = commands.Bot(
  intents=intents,
	command_prefix="!", # Change to desired prefix
	case_insensitive=True # Commands aren't case-sensitive
)

bot.author_id = 692583640538021908 # Change to your discord id!!!

# on_ready events

async def update_status():
  await bot.change_presence(discord.Game(random.choice(activities_playing)))

@bot.event 
async def on_ready(): # When the bot is ready
  print(f"{bot.user} online") # Prints the bot's username and identifier
  # begin an infinite loop for continous tasks
  while True:
    update_status()
    asyncio.sleep(update_frequency)

# on_message events

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
      value = emotes[random.choice(keyword_reactions[keyword])]
      print(f"Reacting to {message.author}: \"{message.content}\" with {value}")
      await message.add_reaction(value) 

async def chain_message(message: discord.Message):
  # save the last 4 messages received
  memory.last_four_messages.insert(0, message)
  if len(memory.last_four_messages) > 4:
    memory.last_four_messages.pop()
  else:
    return
  # check if memory is repetitve 
  for v in memory.last_four_messages[1:]:
    if v.content != memory.last_four_messages[0].content:
      return
  # contribute to the spam
  print(f"Spamming {message.content}")
  await message.channel.send(content=message.content)
  # clear memory
  memory.last_four_messages = []

async def reply_ping(message: discord.Message):
  if "<@1050873792525774921>" in message.content:
    emote_response = emotes[random.choice(greeting_reactions)]
    await message.reply(content=emote_response*random.randint(1,3))

@bot.event
async def on_message(message: discord.Message):
  if message.author == bot.user:
    return
  await react_random(message)
  await react_keywords(message)
  await chain_message(message)
  await reply_ping(message)

extensions = [
	'cogs.cog_example'  # Same name as it would be if you were importing it
]

if __name__ == '__main__':  # Ensures this is the file being ran
	for extension in extensions:
		bot.load_extension(extension) # Loads every extension.

keep_alive()  # Starts a webserver to be pinged.
token = os.environ.get("DISCORD_BOT_SECRET") 
bot.run(token) # Starts the bot