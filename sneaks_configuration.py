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
        "Hatsune Miku: Project DIVA Mega Mix+",
        "Sayonara Wild Hearts",
        "Deep Rock Galactic",
        "Pizza Tower",
        "The Stanley Parable",
        "Papers, Please",
        "Blender",
        "MTGArena",
		"BTD6",
		"EXAPUNKS",
		"CS2",
		"Source Filmmaker",
		"Shadows of Doubt",
		"Hitman: World of Assassination",
		"Vim",
		"Emacs",
		"Subway Surfers",
	    "Peggle Extreme",
        "Balatro"
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
        "Pendulum",
        "the screams of hell",
		"Initial D Soundtrack",
		"Mr. Kitty",
		"Inabakumori",
        "The Weeknd"
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

    # pfps for sneaks to use
    # pfps = [
    #   "sneakers.png",
    #   "sneaks.png",
    #   "sneaks2.png",
    #   "sneaks3.png",
    #   "sneaks4.png",
    #   "sneaks5.png",
    #   "sneaks6.png",
    #   "sneaks7.png",
    # ]

    # brainrot regex, from wikipedia filter 614
    # it is a vandalism filter... so dont be surprised if it has weird shit
    brainrot_regex = r"""(?x)
        \bඞ\b
        |420\s*b+l+a+z+e+\s*i+t+
        |absolute\s*unit
        |[ah]{12,}
        |amog\s*us+\b
        |among\s+us\b.{0,20}\b(?:among\s+us|game|impost[eo]r|ohio|sus\b)
        |amongus+\b
        |aviation\s*,[\s\S]*?there\s*is\s*no[\s\S]*?bee[\s\S]*?be\s*able\s*to\s*fly
        |\bayyy+
        |b+o+iii+
        |baby\sgronk
        |balkan\s+breakfast
        |\bbitch\s*ass\b
        |\b(?:bo[iy]|in\sthe)\s*[bp]uss(?:ies|y)\b
        |\bboobs\b
        # |\bbr(?:[aou]+[hv]+|ooo+)\b
        |bush\s*did\s*9.?11
        |\bcaseoh\b
        |cheese\sdrippy
        |chicken\s*f[u\*]?[c\*]k(?:er|s|ing)?
        |\bching\s*chong\b
        |chung[uea]s\b
        |dQw4w9WgXcQ
        |(?:d[3e](?:[3e]+[sz]+|[sz][sz]*)e*|th[3e][zs$][3e])\s*n+u+t+[zs$]
        |(?<![\#\d])(?:69\D{0,3}420|420\D{0,3}69|(?:69\D{0,3}){3,})(?!\d)
        |dank\s*meme
        |\bdat\s+boi
        |(?:dems?|them[`']?s?|those\s+are)[`']?\s+(?:da|th[ea])\s+fa(?:cts|x)
        |\bdiddler\b
        |\bdiddy(?:[`']?s)?\W+(?:.{0,80}\b(?:(?:any|no)thing\s*wrong|baby\s*oil)|did\w*\W+did\w*|diddy|free|high|house|i|oil|party|school|studios|volumes)\b
        |\bdiddys\b
        |drumpf
        |e+s+k+e+t+i+t
        |\beats?\s*ass\b
        |\b(?:eat|kiss|smack|smell|stick|suck)\w*\s+my\s+(?:arse|ass|balls|big|bog|butt|cock|cum|dic?k|fucking|penis|schlong|shorts|tits|weiner)\b
        |epst(?:ei|ie)n\W+did\s*n.?t\s+kill
        |\berm\swhat\b
        |(?:f[u\*][c\*]k(?:ing?|ed|s)|sex\s*with?)\s*chickens?
        |f\s*r\s*e\s*e\s*d\s*i\s*d\s*d\s*y
        |\bfanum\s*tax
        |\bfem\W?bo[iy]s?\b
        |fetus\s*deletus
        |\bg+a+yy(?:y|\b)
        |german\s+stare
        |\bgooning\b
        |\bgriddy\b
        |gucci\s*gang[\s,]*gucci\s*gang
        |\bgyat\b
        |gyatt
        |\bh(?:ello|i)\smy\sname\b
        |hard\s+(?:pp|peepee)
        |hawk.?tua(?:\w?\b|h)
        |hit\s*or\s*miss[\s,]*I\s*guess
        |hitler\b.{0,40}\b(?:any|no)thing?\s*wrong
        |\s*i\s*n\s*t\s*h\s*[ae]\s*p\s*(?:(?:[@uv*]\s*)+(?:[zs\$*]\s*)+|[zs\$*]{2,})\s*a*y+
        |(?:idi|toilet|what\s+the|ohio)\s+sigma
        |impost[eo]rs?\b.{0,20}\b(?:among\sus|sus\b)
        |is\s+the\s+goat
        |ishowspeed
        |jamaican\s+smiling
        |joe\s+m[oa]m+a
        |(?<!koe\s)\by+ee+t+(?:e+(?:r+|d+))?\b
        |l\s*bozo
        |\bligma\b
        |lo+(?:w*|w\w*)\s+tap+er\s+fade
        |\bnibb+a+\b
        |nick\s*turani
        |\bnonce\b
        |ok(?:ay)?,?\s+boomer
        |\booo+f+\b
        |\bp\.diddy\b
        |\b(?:pee+|poo+)\s*(?:pee+|poo+)\b
        |(?:pp|peepee)\s+hard
        |\bquandale\b
        |\br+eeeeee
        |\b(?:ranboo|tubbo)
        |rawr\s*xd
        |\#redirect\s*\[\[donald[\s_]trump\]\]
        |\brizz+(?:\b|e[rd]|ful|ing|l[ey]|y)
        |\brizz\w*\b.{0,40}\bhuzz\b
        |rizzmas
        |\bs(?:u+i{3,}|i+u{3,})\b
        |s+k+[i1bdt]{4,}y*\b
        |\bs+us+us+\b
        |s+w+[4ae]+gg[g]+
        |\bsigma(?:aa+\w*|s)\b
        |sigma\s+(?:boy|male|ohio|rizz\w*|sigma|sk[bdi]+\b|toilet)
        |skibi[td]{1,2}[iy]
        |smartschoolboy9
        |sub(?:scrib(?:e[ds]?|ing))?\s*(?:2|to)\s*(?:p(?:ew|oo|ud|ue|uw)|te*.?series)
        |\bsussy\b
        |sw[4ae]g\s*(?:yolo|daddy|money|lord|master)
        |\#(?:sw[4ae]g|yolo)
        |\bt+\s*h+\s*i+\s*c\s*c
        |\bt+r+o+l(?:o+l|ll)
        |thick\s+of\s+it,?\s*everybody
        |tran?s?.?manian?\b\bඞ\b
        |420\s*b+l+a+z+e+\s*i+t+
        |absolute\s*unit
        |amog\s*us+\b
        |among\s+us\b.{0,20}\b(?:among\s+us|game|impost[eo]r|ohio|sus\b)
        |amongus+\b
        |aviation\s*,[\s\S]*?there\s*is\s*no[\s\S]*?bee[\s\S]*?be\s*able\s*to\s*fly
        |\bayyy+
        |b+o+iii+
        |baby\sgronk
        |balkan\s+breakfast
        |\bbitch\s*ass\b
        |\b(?:bo[iy]|in\sthe)\s*[bp]uss(?:ies|y)\b
        |\bboobs\b
        # |\bbr(?:[aou]+[hv]+|ooo+)\b
        |bush\s*did\s*9.?11
        |\bcaseoh\b
        |cheese\sdrippy
        |chicken\s*f[u\*]?[c\*]k(?:er|s|ing)?
        |\bching\s*chong\b
        |chung[uea]s\b
        |dQw4w9WgXcQ
        |(?:d[3e](?:[3e]+[sz]+|[sz][sz]*)e*|th[3e][zs$][3e])\s*n+u+t+[zs$]
        |(?<![\#\d])(?:69\D{0,3}420|420\D{0,3}69|(?:69\D{0,3}){3,})(?!\d)
        |dank\s*meme
        |\bdat\s+boi
        |(?:dems?|them[`']?s?|those\s+are)[`']?\s+(?:da|th[ea])\s+fa(?:cts|x)
        |\bdiddler\b
        |\bdiddy(?:[`']?s)?\W+(?:.{0,80}\b(?:(?:any|no)thing\s*wrong|baby\s*oil)|did\w*\W+did\w*|diddy|free|high|house|i|oil|party|school|studios|volumes)\b
        |\bdiddys\b
        |drumpf
        |e+s+k+e+t+i+t
        |\beats?\s*ass\b
        |\b(?:eat|kiss|smack|smell|stick|suck)\w*\s+my\s+(?:arse|ass|balls|big|bog|butt|cock|cum|dic?k|fucking|penis|schlong|shorts|tits|weiner)\b
        |epst(?:ei|ie)n\W+did\s*n.?t\s+kill
        |\berm\swhat\b
        |(?:f[u\*][c\*]k(?:ing?|ed|s)|sex\s*with?)\s*chickens?
        |f\s*r\s*e\s*e\s*d\s*i\s*d\s*d\s*y
        |\bfanum\s*tax
        |\bfem\W?bo[iy]s?\b
        |fetus\s*deletus
        |\bg+a+yy(?:y|\b)
        |german\s+stare
        |\bgooning\b
        |\bgriddy\b
        |gucci\s*gang[\s,]*gucci\s*gang
        |\bgyat\b
        |gyatt
        |\bh(?:ello|i)\smy\sname\b
        |hard\s+(?:pp|peepee)
        |hawk.?tua(?:\w?\b|h)
        |hit\s*or\s*miss[\s,]*I\s*guess
        |hitler\b.{0,40}\b(?:any|no)thing?\s*wrong
        |\s*i\s*n\s*t\s*h\s*[ae]\s*p\s*(?:(?:[@uv*]\s*)+(?:[zs\$*]\s*)+|[zs\$*]{2,})\s*a*y+
        |(?:idi|toilet|what\s+the|ohio)\s+sigma
        |impost[eo]rs?\b.{0,20}\b(?:among\sus|sus\b)
        |is\s+the\s+goat
        |ishowspeed
        |jamaican\s+smiling
        |joe\s+m[oa]m+a
        |(?<!koe\s)\by+ee+t+(?:e+(?:r+|d+))?\b
        |l\s*bozo
        |\bligma\b
        |lo+(?:w*|w\w*)\s+tap+er\s+fade
        |\bnibb+a+\b
        |nick\s*turani
        |\bnonce\b
        |ok(?:ay)?,?\s+boomer
        |\booo+f+\b
        |\bp\.diddy\b
        |\b(?:pee+|poo+)\s*(?:pee+|poo+)\b
        |(?:pp|peepee)\s+hard
        |\bquandale\b
        |\br+eeeeee
        |\b(?:ranboo|tubbo)
        |rawr\s*xd
        |\#redirect\s*\[\[donald[\s_]trump\]\]
        |\brizz+(?:\b|e[rd]|ful|ing|l[ey]|y)
        |\brizz\w*\b.{0,40}\bhuzz\b
        |rizzmas
        |\bs(?:u+i{3,}|i+u{3,})\b
        |s+k+[i1bdt]{4,}y*\b
        |\bs+us+us+\b
        |s+w+[4ae]+gg[g]+
        |\bsigma(?:aa+\w*|s)\b
        |ugandan\s*knuckles
        |[ui]s\s+sus\b
        |\buwu\b
        |\bwo+m+p+\s*wo+m+p+\b
        |\by+o+l+o[lo]+c
        |y\s*o\s*[lo\s]+s\s*w\s*[4ae]+\s*g+
        |\byall\b
        |\b(?:yo)?ur\sm[ou]m\b
        |\byooo+\bm
        |you['`]?ve\s*been\s*gnomed
        |\bmewing\b # why did wikipedia not include this
        |\braise.*(ya+.*){2,}\b # techy says this
        |fine.?sh[iy]t
        |[(negative)(positive)(l)].?aura
        |aura.?farming
        |maxxing\b
        |\bopps\b
        |\b[(the)(da)].?drip
        |\bdrippy.?cheese
        |\b[(kind)(pretty)].*sus
        """
