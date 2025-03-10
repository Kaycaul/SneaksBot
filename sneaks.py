import json
import random
import discord # type: ignore
import time
import datetime
from sneaks_configuration import SneaksConfiguration
from discord.ext import commands # type: ignore
from discord.utils import get # type: ignore
from discord import FFmpegPCMAudio # type: ignore
import os
import asyncio
from websockets.asyncio.client import connect
import glob
import re

class Sneaks():

    # initial values
    doeball_uid = 692583640538021908
    cafe_guild_id = 923788487562493982
    active_role_id = 1054661101029179453
    art_battle_channel = 923801808512647210
    announcements_channel = 923813516970975282
    reaction_chance = 299
    keyword_reaction_chance = 2
    # the number of days until sneaks no longer considers a user "active"
    days_before_inactive = 5
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
    brainrot_regex = re.compile(config.brainrot_regex, re.IGNORECASE)

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
        path = random.choice(glob.glob("ProfileIcons/*"))
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
                # possibly very slow!!
                async for message in channel.history(after=after, limit=10):
                    if not message.author.bot and message.author not in active_users:
                        print("\033[1;36m.", end='', flush=True)
                        active_users.append(message.author)
            except discord.errors.Forbidden:
                # strangely enough, sneaks knows the admin channels exist, but isnt allowed to view them
                blocked_channels += 1
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

    async def stuff2(self, message):
      cleaned_message = message.content.lower()
      if "im stuff" in cleaned_message and random.randint(0, 5) == 0:
        print(f"replying to message from {message.author} with i cant take it")
        await message.reply(content=f"haha {message.author.name} i cant fucking take it anymore")


    async def stuff(self, message):
      cleaned_message = message.content.lower()
      if ((not cleaned_message[-5:] == "stuff") and (not "doing stuff" in cleaned_message)) or random.randint(0, 5) != 3:
        return
      print(f"replying to message from {message.author} with stuff")
      await message.reply(content="im stuff")


    async def eh_ha_heh_heh(self, message):
      cleaned_message = message.content.lower()
      if ((not cleaned_message[-3:] == "off") and (not '"off"' in cleaned_message)) or random.randint(0, 5) != 3:
        return
      print(f"replying to message from {message.author} with eh? ha! heh heh.")
      await message.reply(content="eh? ha! heh heh.")
      await message.add_reaction("<:heh:1248817235129270412>")


    async def play_music(self, message):
        # currently broken, opus not loaded, not willing to deal with this lmao
        if (True):
          return
        ##############
        ##############
        prefix = "sneaksplay "
        prefix_length = len(prefix)
        if not message.content[:prefix_length] == prefix:
            return
        # get the voice channel and user
        user = message.author
        voice = user.voice
        if not voice:
            await message.reply(content="youre not in a vc")
            return
        voice_channel = voice.channel
        received_time = time.time()
        # get only the url
        url = message.content[prefix_length:]
        # run yt-dlp on the url
        try:
            # name the file with the current timestamp
            os.system(
                f'yt-dlp -x --audio-format mp3 --playlist-end 1 -o \"Songs\\{received_time}.mp3\" \"{url}\"')
        except Exception as e:
            print("\033[1;31m" + str(e))
            await message.reply(content="download didnt work")
            return

        # join the vc
        print(f"\033[1;36mJoining {voice_channel.name}")
        voice = voice_channel.guild.voice_client
        if voice and voice.is_connected():
            print(f"\033[1;36mMoving to {voice_channel.name}")
            await voice.move_to(voice_channel)
        else:
            print(f"\033[1;36mConnecting to {voice_channel.name}")
            voice = await voice_channel.connect()

        # play the file in vc with the user
        print(f"\033[1;36mPlaying {received_time}.mp3")
        source = FFmpegPCMAudio(f"Songs\\{received_time}.mp3")
        voice.play(source)

        # wait until finished, delete the file and dc
        while voice.is_playing():
            await asyncio.sleep(1)
        print(f"\033[1;36mDeleting {received_time}.mp3")
        os.remove(f"Songs\\{received_time}.mp3")
        await voice.disconnect()


    async def download_video(self, message):
        prefix = "download "
        prefix_length = len(prefix)
        if not message.content[:prefix_length] == prefix:
            return
        # clear
        if os.path.exists("download.mp4"):
            os.remove("download.mp4")
        # get only the url
        url = message.content[prefix_length:]
        # run yt-dlp on the url
        try:
            os.system(f'yt-dlp -o download.mp4 --playlist-end 1 \"{url}\"')
        except Exception as e:
            print("\033[1;31m" + str(e))
            await message.reply(content="download didnt work")
            return
        # post the message as an attachment
        try:
            await message.reply(file=discord.File(r"download.mp4"))
        except Exception as e:
            print("\033[1;31m" + str(e))
            await message.reply(content="cant send it")
            return
        # delete the file locally
        if os.path.exists("download.mp4"):
            os.remove("download.mp4")
        # i cant beleive this just works its a miracle
        print(f"\033[1;35mDownloaded: {message.content[prefix_length:]}")


    async def echo_message(self, message: discord.Message):
        # echo messages
        if not message.content[0:5] == "echo ":
            return
        # randomly dont because lol
        if random.randint(0, 100) == 69:
            await message.channel.send(content="no lmao")
            await message.channel.send(content="https://cdn.discordapp.com/attachments/923788487562493985/1106443679088001074/xfCCMdjed9FsPAc7AIBLFgEq.png")
            return
        text = message.content[5:].lower()
        await message.channel.send(content=text)
        print(f'\033[1;35mEchoed \"{text}\" from {message.author}')
        await message.delete()


    async def react_random(self, message: discord.Message):

        # randomly abort like 99% of the time
        if random.randint(0, self.reaction_chance) != 0:
            return
        # react with a random known emote
        emote = random.choice(self.all_known_emotes)
        print(
            f'\033[1;35mReacting to {message.author}: \"{message.content}\" with {emote}'
        )
        await message.add_reaction(emote)
        # if it is a good status, set it as your status too
        if 21 > len(message.content) > 2:
            print(f'\033[1;35mStealing \"{message.content}\" as a status')
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
                    f'\033[1;35mReacting to \"{message.content}\" with {value}'
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
            
        # stop him from spamming blank messages which seems to cause so many errors
        if message.content == "":
            return

        # contribute to the spam
        print(f'\033[1;35mSpamming \"{message.content}\"')
        await message.channel.send(content=message.content)


    async def reply_ping(self, message: discord.Message):
        if f"<@{self.bot.user.id}>" in message.content:
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
        if not input.content.lower() == f"<@{self.bot.user.id}> recap":
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


    async def reaction_image(self, message: discord.Message):
        if random.randint(0, 700) != 0:
            return
        # pick a random file and load it
        path = random.choice(glob.glob("ReactionImages/*")) 
        print(f"\033[1;35mSending image {path}")
        file = discord.File(path)
        # send it to discord
        await message.reply(file=file, content="")


    async def brainrot_scan(self, message: discord.Message):
        # ignore bots (to prevent infinite "what the sigma" mutual recursion)
        if message.author.bot: return
        # brainrot detection regex courtesy of wikipedia
        # https://en.wikipedia.org/wiki/Special:AbuseFilter/614
        capture = self.brainrot_regex.search(message.content)
        if capture:
            print(f"Brainrot \"{capture.group(0)}\" caught, by {message.author}")
            await message.reply(content="erm what the sigma")


    # https://www.azuracast.com/docs/developers/now-playing-data/
    # called at the start to loop forever, searching for nowplaying updates
    async def open_websocket(self):
        # lol i dont think ive ever indented something this much
        while True:
            try:
                # get socket url from env file
                websocket_url = os.environ.get("WEBSOCKET_URL")
                async with connect(websocket_url) as websocket:
                    # connect to socket
                    await websocket.send(json.dumps({ "subs": { "station:boing": {} }}))
                    previous_song_id = None
                    while True:
                        # wait for new data
                        res = json.loads(await websocket.recv())
                        # respond to nowplaying data, print if song id has changed
                        if "pub" not in res: continue
                        nowplaying_data = res["pub"]["data"]["np"]["now_playing"]
                        song = nowplaying_data["song"]
                        if previous_song_id == song["id"]: continue
                        previous_song_id = song["id"]
                        await self.post_nowplaying_update(song)
            except Exception as e:
                print(e)


    # post an embed into the designated channel
    async def post_nowplaying_update(self, song):
        # only update if users are in vc in the cafe server with the bot
        anyone_listening = False
        for client in self.bot.voice_clients:
            if client.guild.id != self.cafe_guild_id: continue
            if len(client.channel.members) < 2: continue
            anyone_listening = True
            break
        if not anyone_listening: return
        # post the update
        designated_channel_id = self.config.radio_nowplaying_channel_id
        channel = self.bot.get_channel(designated_channel_id)
        emb = self.get_nowplaying_embed(song)
        await channel.send(embed=emb)


    # takes song json from nowplaying api and returns the appropriate embed to represent it
    # called by websocket update and manually by users
    def get_nowplaying_embed(self, song):
        emb = discord.Embed(title="Now Playing", description=song["text"], color=discord.Color.blue()) # title and artist together
        emb.set_thumbnail(url=song["art"])
        return emb
