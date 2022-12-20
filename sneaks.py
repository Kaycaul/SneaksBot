import random
import discord
import asyncio
from discord.ext import commands

doeball_uid = 692583640538021908
reaction_chance = 99
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
  "Krita",
  "Vrchat",
  "Fancy Pants Adventure",
  "Bubble Tanks",
  "Fireboy and Watergirl",
  "Among Us",
  "Jackbox Party Pack 7",
  "Bloons TD6",
  "with a ball of yarn"
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

class Sneaks():

    def __init__(self):
        self.last_four_messages = []
        # set up the bot
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        intents.presences = True
        self.bot = commands.Bot(
            intents=intents,
            command_prefix="!", # Change to desired prefix
            case_insensitive=True # Commands aren't case-sensitive
        )
        # configure the bot
        self.bot.author_id = doeball_uid

    # on_ready events, occur as loops

    async def update_status(self, frequency):
        while True:
            # choose a new activity to play from the list
            new_activity_name = random.choice(activities_playing)
            print(f"Switching status to 'Playing {new_activity_name}'")
            # update the presence
            await self.bot.change_presence(activity=discord.Game(new_activity_name))
            # wait some amount of time before trying again
            await asyncio.sleep(frequency)
    
    # on_message events

    async def react_random(self, message: discord.Message):
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

    async def react_keywords(self, message: discord.Message):
        # react to keywords
        for keyword in keyword_reactions.keys():
            # if the key is in the message
            if keyword in message.content.lower():
                # react with the value of the key
                value = emotes[random.choice(keyword_reactions[keyword])]
                print(f"Reacting to {message.author}: \"{message.content}\" with {value}")
                await message.add_reaction(value) 

    async def chain_message(self, message: discord.Message):
        # save the last 4 messages received
        self.last_four_messages.insert(0, message)
        if len(self.last_four_messages) > 4:
            self.last_four_messages.pop()
        else:
            return
        # check if memory is repetitve 
        for v in self.last_four_messages[1:]:
            if v.content != self.last_four_messages[0].content:
                return
        # contribute to the spam
        print(f"Spamming {message.content}")
        await message.channel.send(content=message.content)
        # clear memory
        self.last_four_messages = []

    async def reply_ping(self, message: discord.Message):
        if "<@1050873792525774921>" in message.content:
            emote_response = emotes[random.choice(greeting_reactions)]
            await message.reply(content=emote_response*random.randint(1,3))