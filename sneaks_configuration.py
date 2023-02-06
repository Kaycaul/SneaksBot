class SneaksConfiguration:
    greeting_reactions = ["bl", "boil", "hard", "matt", "sack", "gloglet", "sneakers"]

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
        "Bubble Tanks 2",
        "Fireboy and Watergirl",
        "Among Us",
        "Jackbox Party Pack 7",
        "Bloons TD6",
        "with a ball of yarn",
        "Genshin Impact",
        "Skyfactory 4",
        "FTB Academy",
        "Create - Fabric 1.19.2",
        "Blaseball",
        "Dwarf Fortress",
        "No Mans Sky",
        "Getting Over It",
        "Spaceteam",
        "Shenzhen I/O",
        "slither.io",
        "agar.io",
        "Powder Game",
        "Subnautica",
        "Full of Stars",
        "Undertale",
        "Deltarune",
        "Trackmania",
        "Cookie Clicker",
        "BFDIA 5b",
        "Worms Armageddon",
        "Tokobot",
        "Trove",
        "Deltarune",
        "Windows 93",
        "lego power miners",
        "Hatsune Miku: Project DIVA Mega Mix+"
        
    ]

    # list of activites that are songs for sneaks to listen to
    activities_listening = [
        "Porter Robinson",
        "Madeon",
        "Mariah Carey",
        "FM-84",
        "The Midnight",
        "Disasterpeace",
        "Fearofdark",
        "DaymanOurSaviour",
        "Mariya Takeuchi",
        "Windows96",
        "Protodome",
        "Tally Hall",
        "Lemon Demon",
        "Toshiki Kadomatsu",
        "HOME",
        "A.L.I.S.O.N",
        "猫 シ Corp.",
        "Pilotredsun",
        "K/DA",
        "Tycho",
        "Caramelldansen",
        "MACINTOSH PLUS",
        "C418",
        "Masayoshi Takanaka",
        "Tatsuro Yamashita",
        "Hallmark '87",
        "TOWERS",
        "youtu.be/dQw4w9WgXcQ",
        "Pendulum"
    ]

    # sneaks should not be able to use these emotes
    emote_blacklist = [
        # i thought it could potentially result in awkward rather than funny reactions if these were included lol
        "<a:petpat_Tiran:1032305183461486622>", 
        "<a:petpat_Techy:1003543375120695296>",
        "<a:petpat_Myri:1014733264822489098>",
        "<a:chromapet:1004604447781036082>",
        # the trophy emotes arent very funny and usually just dont make sense
        "<:trophy_concept:991050295490514954>",
        "<:trophy_cool:991050294467121172>",
        "<:trophy_cute:991050293401772102>",
        "<:trophy_effort:991050296526516275>",
        "<:trophy_funny:969750249721720882>"
    ]

    # sneaks should be able to use only these stock emoji
    emoji_whitelist = [
        "🚫",
        "❌",
        "💕",
        "™",
        "⭐",
        "🍔",
        "👍",
        "👎",
        "🤓",
        "\U0001FAF5", # pointing at viewer
        "🧱",
        "🇨🇦",
        "\U0001f3f3\uFE0F\u200D\U0001f308",
        "🏳️‍⚧️"

    ]

    # dictionary of emotes and their ids
    emotes = {
        "presence" : "<:presence:941828627807490048>",
        "bl" : "<:bl:996875747346100354>",
        "boil" : "<a:boil:1045540000600698980>",
        "hard" : "<:hard:924072022777167912>",
        "fuckyou" : "<a:fuckyou:1045005787451375687>",
        "matt" : "<:matt:1031681843600293949>",
        "sack" : "<:sack:924512985504960552>",
        "resentment" : "<:resentment:924072022160584704>",
        "okay" : "<:okay:936301680746700810>",
        "gloglet" : "<a:gloglet:1040418817119092806>",
        "sneakers" : "<:sneakers:1064268113434120243>",
        "ratio" : "<:ratio:1072002164479770704>",
    }

    # dictionary of what emotes to use to react to which messages
    keyword_reactions = {
        "d20" : ["presence", "fuckyou", "resentment", "okay"],
        "sneak" : greeting_reactions,
        "snuck" : greeting_reactions,
        "ratio" : ["ratio"],
        "alex" : ["ratio"],
    }

    # ids of the trophy emotes, searched for in the art battle recap
    trophies = [
        969750249721720882,
        991050295490514954,
        991050296526516275,
        991050294467121172,
        991050293401772102
    ]