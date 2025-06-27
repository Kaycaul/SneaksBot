from logging import config
import os
import discord # type: ignore
from discord import app_commands # type: ignore
import asyncio
# from keep_alive import keep_alive
from sneaks import Sneaks
import requests

import pymongo # type: ignore
from bson.objectid import ObjectId
from pymongo.results import UpdateResult
from datetime import datetime, timezone
import requests
import youtube_dl
from sneaks_configuration import SneaksConfiguration

print(f"running discord api {discord.__version__}")

print(f"Connecting to mongo server")
client = pymongo.MongoClient("mongodb://127.0.0.1:27017")
db = client["website"]
artworks_collection = db["artworks"]

# create a new sneaksbot
sneaksbot = Sneaks()
bot = sneaksbot.bot

@bot.event
async def on_ready():  # When the bot is ready
    print(f"\033[1;93m{bot.user} online\nLoggers!!")  # Prints the bot's username and identifier 
    await sneaksbot.update_known_emotes()
    # sync slash commands
    await bot.tree.sync(guild=discord.Object(id=923788487562493982))
    # open websocket to get nowplaying data from radio
    background_tasks = set()
    task = asyncio.create_task(sneaksbot.open_websocket())
    background_tasks.add(task) # prevent the task from being garbage collected
    # begin all the infinitely looping coroutines, execute them once per second
    while True:
        #await sneaksbot.update_active_role(3600) # this will recur every hour
        await sneaksbot.update_status(600) # this will recur every 10 minutes
        await sneaksbot.update_profile(3000)
        await asyncio.sleep(1)


@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return
    await sneaksbot.stuff(message)
    await sneaksbot.stuff2(message)
    # await sneaksbot.play_music(message)
    #await sneaksbot.download_video(message)
    await sneaksbot.echo_message(message)
    await sneaksbot.react_random(message)
    await sneaksbot.react_keywords(message)
    await sneaksbot.chain_message(message)
    await sneaksbot.reply_ping(message)
    await sneaksbot.emote_dump(message) # this was a mistake
    await sneaksbot.art_battle_recap(message)
    await sneaksbot.reaction_image(message)
    await sneaksbot.eh_ha_heh_heh(message)
    await sneaksbot.brainrot_scan(message)

@bot.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    # disconnect if the channel the user was in, is the channel i am in, and if nobody is left now
    for client in bot.voice_clients:
        if before.channel != client.channel: continue
        # we found the channel the user just left
        if len(client.channel.members) == 1: # nobody else is left
            await client.disconnect()
            return

# I HAVE NO IDEA HOW THE RADIO CODE WORKS BUT IT WORKS
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn',
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

# ????????????????????????????????????
# this is a miracle from god
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

@bot.tree.command(
    name="nowplaying", 
    description="what is currently playing on the radio?",
    guild=discord.Object(id=923788487562493982)
)
async def now_playing(interaction: discord.Interaction):
    try:
        # request the radio url from {url}/api/nowplaying/ (only works for azuracast)
        nowplaying_url = os.environ.get("NOWPLAYING_URL")
        res = await asyncio.to_thread(requests.get, nowplaying_url)
        if not res.status_code == 200:
            await interaction.response.send_message(f"<:sneakers:1064268113434120243>❌ response code: `{res.status_code}`")
            return
        response_data = res.json()[0]
        song = response_data["now_playing"]["song"]
        emb = sneaksbot.get_nowplaying_embed(song)
        await interaction.response.send_message(embed=emb)
    except Exception as e:
        await interaction.response.send_message(f"<:sneakers:1064268113434120243>❌ exception:\n```\n{e}```")
        raise

# https://github.com/Rapptz/discord.py/blob/master/examples/basic_voice.py
@bot.tree.command(
    name="radiojoin", 
    description="join your vc and play songs forever from the radio",
    guild=discord.Object(id=923788487562493982)
)
async def radio_join(interaction: discord.Interaction):
    try:
        radio_url = os.environ.get("RADIO_URL")
        voice = interaction.user.voice
        if not voice:
            await interaction.response.send_message("<:sneakers:1064268113434120243>❌ join vc first")
            return
        channel = voice.channel
        vc = await channel.connect()
        # i think this makes a new one each time and leaks the previous one or something... idk how it works
        radio_player = await YTDLSource.from_url(radio_url, loop=bot.loop, stream=True)
        vc.play(radio_player, after=lambda e: print(f'Player error: {e}') if e else None)
        await interaction.response.send_message("<:sneakers:1064268113434120243> done")
    except Exception as e:
        await interaction.response.send_message(f"<:sneakers:1064268113434120243>❌ exception:\n```\n{e}```")
        raise

@bot.tree.command(
    name="radioleave", 
    description="disconnect the bot from a vc",
    guild=discord.Object(id=923788487562493982)
)
async def radio_leave(interaction: discord.Interaction):
    user_vc = interaction.user.voice.channel
    if user_vc:
        # find the vc in my clients
        for client in bot.voice_clients:
            if client.channel == user_vc:
                await client.disconnect()
                await interaction.response.send_message("<:sneakers:1064268113434120243>👍")
                return
    await interaction.response.send_message(f"<:sneakers:1064268113434120243>❌ u gotta be in vc with me bro")
    
@bot.tree.command(
    name="post", 
    description="Posts an art image to my website and it only works for my account hahahaha",
    guild=discord.Object(id=923788487562493982)
)
@app_commands.describe(url="the image you want to post (url)")
@app_commands.describe(artist="name of the artist")
@app_commands.describe(tags="space-separated tags")
@app_commands.describe(filename="what to change the filename to")
async def post(interaction: discord.Interaction, url: str, artist: str, tags: str, filename: str):
    await interaction.response.send_message(content="<:sneakers:1064268113434120243> Thinking...")
    try:
        # break if user doesnt have doeball uid
        if interaction.user.id != sneaksbot.doeball_uid:
            await interaction.followup.send("<:sneakers:1064268113434120243>❌")
            return
        # save image to the servers folder (stupid design because sneaksbot wasnt messy enough)
        root = "./"
        # regex the image name at the end of the url
        directory = "uploads/"
        file = os.path.basename(url).split("?")[0]
        ext = file.split(".")[1]
        save_path = f"{root}{directory}{filename}.{ext}"
        print(f"saving the image at {url} to {save_path}")
        # never overwrite
        if (os.path.exists(save_path)):
            await interaction.followup.send("file already exists dumbass rename it or something <:sneakers:1064268113434120243>❌")
            return
        with open(save_path, "wb") as handle:
            try:
                content = requests.get(url).content
                handle.write(content)
            except Exception as e:
                if os.path.exists(save_path):
                    os.remove(save_path)
                await interaction.followup.send(f"<:sneakers:1064268113434120243>❌ exception accessing url:\n`{e}`")
                return
        try:
            # with the new path, put the image path in the database with the metadata
            taglist = tags.split(" ")
            newpost = {
                "path": f"/assets/uploads/{filename}.{ext}",
                "artist": artist,
                "tags": taglist,
                "date": datetime.now(timezone.utc)
            }
            _id = artworks_collection.insert_one(newpost)
            res = f"\"{filename}\" by {artist}\ntags: {taglist}\nInserted @ {_id.inserted_id}\nhttps://meow.doeball.ca/gallery?artist={artist}\n<:sneakers:1064268113434120243>✅"
            await interaction.followup.send(res)
        except Exception as e:
            # delete the file
            if os.path.exists(save_path):
                os.remove(save_path)
            # something went wrong inserting the document
            await interaction.followup.send(f"<:sneakers:1064268113434120243>❌ exception inserting document:\n`{e}`")
            return
    except Exception as e:
        await interaction.followup.send(f"<:sneakers:1064268113434120243>❌ exception:\n`{e}`")

@bot.tree.command(
    name="add_tag_gallery", 
    description="add a tag to a gallery post (doeball only)",
    guild=discord.Object(id=923788487562493982)
)
@app_commands.describe(object_id="the mongodb object id of the post")
@app_commands.describe(tag_name="the tag to add")
async def post(interaction: discord.Interaction, object_id: str, tag_name: str):
    await interaction.response.send_message(content="<:sneakers:1064268113434120243> urrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr...")
    try:
        # break if user doesnt have doeball uid
        if interaction.user.id != sneaksbot.doeball_uid:
            await interaction.followup.send("<:sneakers:1064268113434120243>❌")
            return
        # with the new path, put the image path in the database with the metadata
        artworks_collection.update_one({"_id": ObjectId(object_id)}, {"$push": {"tags": tag_name}})
        await interaction.followup.send("done\n<:sneakers:1064268113434120243>✅")
    except Exception as e:
        await interaction.followup.send(f"<:sneakers:1064268113434120243>❌ exception:\n`{e}`")

# keep_alive()  # Starts a webserver to be pinged.
token = os.environ.get("DISCORD_BOT_SECRET")
bot.run(token)  # Starts the bot