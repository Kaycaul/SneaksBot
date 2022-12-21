class SneaksConfiguration:
    greeting_reactions = ["bl", "boil", "hard", "matt", "sack", "gloglet"]

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
    ]

    # sneaks should not be able to use these emotes
    emote_blacklist = [
        # i thought it could potentially result in awkward rather than funny reactions if these were included lol
        "<a:petpat_Tiran:1032305183461486622>", 
        "<a:petpat_Techy:1003543375120695296>",
        "<a:petpat_Myri:1014733264822489098>",
        "<a:chromapet:1004604447781036082>"
    ]

    # sneaks should be able to use only these stock emoji
    emoji_whitelist = [
        ":no_entry_sign:",
        ":x:",
        ":two_hearts",
        ":tm:",
        ":star:",
        ":hamburger:",
        ":thumbsup:",
        ":thumbsdown:",
        ":index_pointing_at_the_viewer:",
        ":nerd:",
        ":face_with_raised_eyebrow:",
        ":bricks:",
        ":flag_ca:",
        ":rainbow_flag:",
        ":transgender_flag:"

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
        "gloglet" : "<a:gloglet:1040418817119092806>"
    }

    # dictionary of what emotes to use to react to which messages
    keyword_reactions = {
        "d20" : ["presence", "fuckyou", "resentment", "okay"],
        "sneak" : greeting_reactions,
        "snuck" : greeting_reactions
    }