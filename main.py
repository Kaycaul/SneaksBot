import os
import discord # type: ignore
from discord import app_commands # type: ignore
import asyncio
# from keep_alive import keep_alive
from sneaks import Sneaks

import pymongo # type: ignore
from datetime import datetime, timezone
import requests

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
    await sneaksbot.play_music(message)
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

@bot.tree.command(
    name="post", 
    description="Posts an art image to my website and it only works for my account hahahaha",
    guild=discord.Object(id=923788487562493982)
)
@app_commands.describe(url="the image you want to post (url)")
@app_commands.describe(artist="name of the artist")
@app_commands.describe(tags="space-separated tags")
@app_commands.describe(filename="what to change the filename to")
async def post(interaction, url: str, artist: str, tags: str, filename: str):
    await interaction.response.send_message(content=f"<:sneakers:1064268113434120243> Thinking...")
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

# keep_alive()  # Starts a webserver to be pinged.
token = os.environ.get("DISCORD_BOT_SECRET")
bot.run(token)  # Starts the bot