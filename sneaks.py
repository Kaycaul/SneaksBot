import random
import discord
import time
import datetime
from sneaks_configuration import SneaksConfiguration
from discord.ext import commands
from discord.utils import get


class Sneaks():

    # initial values
    doeball_uid = 692583640538021908
    cafe_guild_id = 923788487562493982
    active_role_id = 1054661101029179453
    art_battle_channel = 923801808512647210
    announcements_channel = 923813516970975282
    reaction_chance = 299
    keyword_reaction_chance = 2
    days_before_inactive = 5  # the number of days until sneaks no longer considers a user "active"
    update_status_timestamp = 0
    update_active_role_timestamp = 0
    update_profile_timestamp = 0
    all_known_emotes = [
    ]  # this will contain every emote and emoji sneaks has access to
    # config and configs
    config = SneaksConfiguration()
    activities_playing = config.activities_playing
    activities_listening = config.activities_listening
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
        command_prefix="!",  # Change to desired prefix
        case_insensitive=True  # Commands aren't case-sensitive
    )
    # configuring the bot
    bot.author_id = doeball_uid

    # on ready events, occur outside a loop (only once)
    async def update_known_emotes(self):
        # collect all emotes from every guild
        for guild in self.bot.guilds:
            for emote in [str(e) for e in guild.emojis]:
                if emote in self.config.emote_blacklist:
                    continue
                if emote in self.all_known_emotes:
                    continue
                # add the new emote to the list
                self.all_known_emotes.append(emote)
        # add emoji that are known
        self.all_known_emotes += self.config.emoji_whitelist
        print(
            f"\033[1;36mCollected \033[1;34m{len(self.all_known_emotes)} \033[1;36memotes"
        )

    # on_ready events, occur inside a loop

    async def update_profile(self, frequency):
      # return if too early
      if time.time() - self.update_profile_timestamp < frequency:
        return

      # choose a new profile picture
      path = "ProfileIcons/" + random.choice(self.config.pfps)
      print("\033[1;36mUpdating profile picture to \033[1;34m'" + path + "'")
      fp = open(path, 'rb')
      pfp = fp.read()
      
      # set the profile picture
      await self.bot.user.edit(avatar=pfp)

      # new timestamp
      self.update_profile_timestamp = time.time()

    async def update_status(self, frequency):
        # return if too early
        if time.time() - self.update_status_timestamp < frequency:
            return
        # choose a new activity to play from the lists
        probability_of_listening = len(self.activities_listening) / (
            len(self.activities_playing) + len(self.activities_listening))
        if random.random() < probability_of_listening:
            # random artist
            new_activity_name = random.choice(self.activities_listening)
            print(
                f"\033[1;36mSwitching status to \033[1;34m'Listening to {new_activity_name}'"
            )
            new_activity = discord.Activity(name=new_activity_name, type=2)
        else:
            # random game
            new_activity_name = random.choice(self.activities_playing)
            print(
                f"\033[1;36mSwitching status to \033[1;34m'Playing {new_activity_name}'"
            )
            new_activity = discord.Game(new_activity_name)
        # update the presence
        await self.bot.change_presence(activity=new_activity)
        # save the time
        self.update_status_timestamp = time.time()

    async def update_active_role(self, frequency):
        # return if too early
        if time.time() - self.update_active_role_timestamp < frequency:
            return
        # track the time (for logging of course)
        start_time = time.time()
        print("\033[1;36mUpdating the active role!")
        # compute the range of dates to scan, before today, after a couple days ago
        before = datetime.datetime.today()
        after = before - datetime.timedelta(days=self.days_before_inactive)
        # scan every channel and every message in those channels and note each user found
        print("\033[1;36mSearching for active users", end='', flush=True)
        active_users: list[discord.Member] = []
        guild = self.bot.get_guild(self.cafe_guild_id)
        blocked_channels = 0
        for channel in guild.text_channels:
            try:
                # SOMETHING IS WRONG WITH THE DATE!!! the date is seemingly calculated correctly
                # the role is assigned correctly
                # he is not able to see every message inside the date
                # something is wrong with these arguments somehow
                # I HAVE NO IDEA WHY THIS WORKS NOW, i replaced the after argument with limit 10000, its slow but works
                async for message in channel.history(after=after, limit=10):  # possibly very slow!!
                    if not message.author.bot and message.author not in active_users:
                        print("\033[1;36m.", end='', flush=True)
                        active_users.append(message.author)
            except discord.errors.Forbidden:
                blocked_channels += 1  # strangely enough, sneaks knows the admin channels exist, but isnt allowed to view them
        print(
            f"\n\033[1;36mFound \033[1;34m{len(active_users)} \033[1;36mactive users. Access denied to \033[1;34m{blocked_channels} \033[1;36mchannels."
        )
        # update the role
        print("\033[1;36mAssigning the role", end='')
        role: discord.Role = get(guild.roles, id=self.active_role_id)
        # remove newly inactive members
        for user in role.members:
            if (user not in active_users
                    and user in guild.members) and not user == self.bot.user:
                await user.remove_roles(role)
                print(
                    f"\n\033[1;36mRemoved active role from \033[1;34m{user.name}",
                    end='')
            print("\033[1;36m.", end='', flush=True)
        # add newly active members
        for user in active_users:
            if user not in role.members and user in guild.members:
                await user.add_roles(role)
                print(
                    f"\n\033[1;36mAssigned active role to \033[1;34m{user.name}",
                    end='')
            print("\033[1;36m.", end='', flush=True)
        # done!
        print(
            f"\n\033[1;36mDone updating active role! Time elapsed: \033[1;34m{int(time.time() - start_time)}s"
        )
        self.update_active_role_timestamp = time.time()

    # on_message events

    async def echo_message(self, message: discord.Message):
      # echo messages
      if not message.content[0:5] == "echo ":
        return
      # randomly dont because lol
      if random.randint(0,100) == 69:
        await message.channel.send(content="no lmao")
        await message.channel.send(content="https://cdn.discordapp.com/attachments/923788487562493985/1106443679088001074/xfCCMdjed9FsPAc7AIBLFgEq.png")
        return
      text = message.content[5:].lower()
      await message.channel.send(content=text)
      print(f"\033[1;35mEchoed \"{text}\" from {message.author}")
      await message.delete()

    async def react_random(self, message: discord.Message):
        
        # randomly abort like 99% of the time
        if random.randint(0, self.reaction_chance) != 0:
            return
        # react with a random known emote
        emote = random.choice(self.all_known_emotes)
        print(
            f"\033[1;35mReacting to {message.author}: \"{message.content}\" with {emote}"
        )
        await message.add_reaction(emote)
        # if it is a good status, set it as your status too
        if 21 > len(message.content) > 2:
            print(f"\033[1;35mStealing \"{message.content}\" as a status")
            await self.bot.change_presence(
                activity=discord.Game(message.content)
            )  # use it as your status for now, it will be updated in like 10 minutes

    async def react_keywords(self, message: discord.Message):
        # react to keywords
        for keyword in self.keyword_reactions.keys():
            # randomly break here
            if random.randint(0, self.keyword_reaction_chance) != 0:
                continue
            # if the key is in the message
            if keyword in message.content.lower():
                # react with the value of the key
                value = self.emotes[random.choice(
                    self.keyword_reactions[keyword])]
                print(
                    f"\033[1;35mReacting to \"{message.content}\" with {value}"
                )
                await message.add_reaction(value)

    async def chain_message(self, message: discord.Message):

        # check if the last 4 messages in the channel are identical
        # or if sneaks has already spoken recently, and is found in the history
        history = [m async for m in message.channel.history(limit=4)]
        while len(history) > 0:
            m = history.pop(0)
            if m.content != message.content or m.author == self.bot.user:
                return

        # contribute to the spam
        print(f"\033[1;35mSpamming \"{message.content}\"")
        await message.channel.send(content=message.content)

    async def reply_ping(self, message: discord.Message):
        if "<@1050873792525774921>" in message.content:
            emote_response = self.emotes[random.choice(
                self.greeting_reactions)]
            print(f"\033[1;35mReplying to mention from {message.author}")
            await message.reply(content=emote_response * random.randint(1, 3))

    # prints every emote, mostly for testing but also probably funny
    async def emote_dump(self, message: discord.Message):
        if not "spam me with every emote you know please" in message.content.lower(
        ):
            return
        # print every known message
        message_to_send = ""
        for emote in self.all_known_emotes:
            message_to_send += emote
            if len(message_to_send) > 1000:
                await message.reply(content=message_to_send)
                message_to_send = ""
        await message.reply(content=message_to_send)

    # copies the most awarded posts from #art-battle to #announcements, on demand
    async def art_battle_recap(self, input: discord.Message):
        if not input.content.lower() == "<@1050873792525774921> recap":
            return
        if not input.channel.id == self.announcements_channel:
            return
        print("\033[1;32mStarting art battle recap!")
        # get a history of every message in art battle, from the last calendar month
        art_battle: discord.TextChannel = self.bot.get_channel(
            self.art_battle_channel)
        today = datetime.datetime.today()
        last_month = today.month - 1 if today.month != 1 else 12
        year = today.year if last_month != 12 else today.year - 1
        start = datetime.datetime(year=year, month=last_month, day=1)
        end = datetime.datetime(year=today.year, month=today.month, day=1)
        history = [
            m async for m in art_battle.history(before=end, after=start)
        ]
        # for each trophy emote, find the message with the most
        top_attacks = []
        for trophy in [
                self.bot.get_emoji(emoji) for emoji in self.config.trophies
        ]:
            print(f"\033[1;32mSearching for best {trophy.name} post")
            # find the top message for this trophy
            top_message = history[0]
            most_reactions = 0
            for message in history:
                # find the trophy in question for this message
                for reaction in message.reactions:
                    if reaction.emoji != trophy:
                        continue
                    # if this one is better, it is the new best
                    if reaction.count > most_reactions:
                        top_message = message
                        most_reactions = reaction.count
            # quickly check the best messages dont have zero reactions (nobody won)
            if most_reactions == 0:
                print("\033[1;32mCould not find any!")
                continue
            # add the message to the top attacks
            print(f"\033[1;32mFound a message by {top_message.author}")
            top_attacks.append(top_message)
        # quickly check that the same message does not appear twice (it won twice)
        top_attacks = list(dict.fromkeys(top_attacks))
        # post each in announcements, along with the author, content, and number of each trophy.
        announcements: discord.TextChannel = self.bot.get_channel(
            self.announcements_channel)
        for attack in top_attacks:
            # assemble a message for this top attack
            # include the author
            content = f"<@{attack.author.id}> got "
            # include the number of each trophy
            for trophy in [
                    self.bot.get_emoji(emoji) for emoji in self.config.trophies
            ]:
                for reaction in attack.reactions:
                    if reaction.emoji != trophy:
                        continue
                    content += f"{reaction.count} <:{trophy.name}:{trophy.id}> "
            # include the content of the original message
            content += f"\"*{attack.content}*\""
            # add links to each attachment
            for attachment in attack.attachments:
                content += f" {attachment.url}"
            # post the message
            await announcements.send(content=content)
        print(f"\033[1;32mFinished art battle recap!")
