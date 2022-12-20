import random
import discord
import asyncio
import time
import datetime
from sneaks_configuration import SneaksConfiguration
from discord.ext import commands

class Sneaks():

    # initial values
    doeball_uid = 692583640538021908
    cafe_guild_id = 923788487562493982
    reaction_chance = 99
    days_before_inactive = 1 # the number of days until sneaks no longer considers a user "active"
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

    async def update_active_role(self, frequency):
        start_time = time.time()
        print("Updating active role!")
        # compute the range of dates to scan
        before = datetime.datetime.today()
        after = before - datetime.timedelta(days=self.days_before_inactive)
        # scan every channel and every message in those channels and note each user found
        active_users = []
        guild = self.bot.get_guild(self.cafe_guild_id)
        for channel in guild.text_channels:
            try:
                async for message in channel.history(before=before, after=after): # possibly very slow!!
                    if not message.author.bot and message.author not in active_users:
                        active_users.append(message.author)
            except discord.errors.Forbidden:
                print("Forbidden!")
        # print the list
        print("Active users:")
        [print(user.name) for user in active_users]
        print(f"Done updating active role! Time elapsed: {time.time() - start_time}s")
        await asyncio.sleep(frequency)

    async def react_random(self, message: discord.Message):
        # randomly abort like 99% of the time
        if random.randint(0, self.reaction_chance) != 0:
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