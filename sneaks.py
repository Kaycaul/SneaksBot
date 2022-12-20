import random
import discord
import asyncio
from sneaks_configuration import SneaksConfiguration
from discord.ext import commands

class Sneaks():

    # initial values
    doeball_uid = 692583640538021908
    reaction_chance = 99
    last_four_messages = []
    # config and configs
    config = SneaksConfiguration()
    activities_playing = config.activities_playing
    emotes = config.emotes
    greeting_reactions = config.greeting_reactions
    keyword_reactions = config.keyword_reactions

    # setting up the bot
    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True
    intents.presences = True
    bot = commands.Bot(
        intents=intents,
        command_prefix="!", # Change to desired prefix
        case_insensitive=True # Commands aren't case-sensitive
    )
    # configuring the bot
    bot.author_id = doeball_uid

    # on_ready events, occur as loops

    async def update_status(self, frequency):
        while True:
            # choose a new activity to play from the list
            new_activity_name = random.choice(self.activities_playing)
            print(f"Switching status to 'Playing {new_activity_name}'")
            # update the presence
            await self.bot.change_presence(activity=discord.Game(new_activity_name))
            # wait some amount of time before trying again
            await asyncio.sleep(frequency)
    
    # on_message events

    async def react_random(self, message: discord.Message):
        # randomly abort like 99% of the time
        if random.randint(0, self.config.reaction_chance) != 0:
            return
        if not isinstance(message.channel, discord.DMChannel):
            # select a random guild emoji
            emoji = random.choice(message.guild.emojis)
        else:
            emoji = self.emotes[random.choice(self.emotes.keys())]
        # react with the emoji if you find it
        if emoji:
            print(f"Reacting to {message.author}: \"{message.content}\" with {emoji}")
            await message.add_reaction(emoji)

    async def react_keywords(self, message: discord.Message):
        # react to keywords
        for keyword in self.keyword_reactions.keys():
            # if the key is in the message
            if keyword in message.content.lower():
                # react with the value of the key
                value = self.emotes[random.choice(self.keyword_reactions[keyword])]
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
            emote_response = self.emotes[random.choice(self.greeting_reactions)]
            await message.reply(content=emote_response*random.randint(1,3))