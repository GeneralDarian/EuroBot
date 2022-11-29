import logging

from tools import findOfTheWeek

emote_id = findOfTheWeek.EMOTE_ID


def emojiReplacer(t: str) -> str:
    """Given a string will replace all !<country_code> with their respective emoji. If there is no emoji present, it just returns the string.
    DO NOT LOWERCASE TEXT BEFORE PUTTING INTO FUNCTION!
    Yes I know this can be more efficient but I am too lazy to do it! Let me improve it later
    Input: string
    Output: string"""

    final = t
    # 🇦🇩 🇦🇹 🇧🇪 🇨🇾 🇪🇪 🇫🇮 🇫🇷 🇩🇪 🇬🇷 🇮🇪 🇮🇹 🇱🇻 🇱🇹 🇱🇺 🇲🇹 🇳🇱 🇵🇹 🇸🇰 🇸🇮 🇪🇸 🇪🇺 🇭🇷 🇲🇨 🇻🇦 🇸🇲
    codeToEmote = {
        "!AN": "🇦🇩",
        "!AT": "🇦🇹",
        "!BE": "🇧🇪",
        "!CY": "🇨🇾",
        "!EE": "🇪🇪",
        "!FI": "🇫🇮",
        "!FR": "🇫🇷",
        "!DE": "🇩🇪",
        "!GR": "🇬🇷",
        "!IE": "🇮🇪",
        "!IT": "🇮🇹",
        "!LV": "🇱🇻",
        "!LT": "🇱🇹",
        "!LU": "🇱🇺",
        "!MT": "🇲🇹",
        "!NL": "🇳🇱",
        "!PT": "🇵🇹",
        "!SK": "🇸🇰",
        "!SI": "🇸🇮",
        "!ES": "🇪🇸",
        "!EU": "🇪🇺",
        "!HR": "🇭🇷",
        "!MC": "🇲🇨",
        "!VA": "🇻🇦",
        "!SM": "🇸🇲",
    }
    for i in codeToEmote:
        if i == t:
            final = final.replace(i, codeToEmote[i])

    return final


def get_multiple_result_desc(processed_results: dict) -> str:
    """Given a processed result dict, returns the processed string for display in the discord multiple search results embed.
    Inputs:
    - processed_results (dict): returned from calling coinData.searchProcessor()
    Outputs:
    - desc (str): String to put in the search results embed desc, returns error msg if something went wrong"""
    # {'Status': '0', 'Issuer': '', 'Type': '', 'Year': ''}
    desc = ""
    if processed_results["Issuer"].lower() in country_to_french:
        french_country = country_to_french[processed_results["Issuer"].lower()]
        desc = f"{french_to_genitive[french_country].upper()} {french_to_emoji[french_country]}"
    elif processed_results["Issuer"].lower() in country_id_to_french:
        french_country = country_id_to_french[processed_results["Issuer"].lower()]
        desc = f"{french_to_genitive[french_country].upper()} {french_to_emoji[french_country]}"
    else:
        desc = "Error: Could not fetch country from textHelp"
        return desc

    if (
        processed_results["Type"] is not None
        and processed_results["Type"].lower() in to_type
    ):
        type = to_type[processed_results["Type"].lower()]
        desc = f"{desc} {type}"
    desc = f"{desc} Coins"

    if processed_results["Year"] is not None:
        desc = f"{desc} minted in {processed_results['Year']}"

    return desc


def tocoin_argument_processor(content: str) -> dict:
    """Processes a list of arguments"""

    arguments = {"Status": None, "Sigma": 1, "Intensity": 5, "NMD": 4}

    if content is None:  # base case, if no arguments were supplied
        return arguments

    content_list = content.split()
    already_sigma = False
    already_intensity = False
    already_NMD = False

    for index, value in enumerate(content_list):
        if (
            value.lower() == "-s" and already_sigma == False
        ):  # Try to fetch the sigma value
            try:
                sigma = float(content_list[index + 1])
                if sigma > 10 or sigma < 0:
                    sigma = 0.1
                arguments["Sigma"] = sigma
                already_sigma = True
            except ValueError:  # If -s is not int
                arguments[
                    "Status"
                ] = "Invalid sigma (-s) argument given [argument must be a number]"
                return arguments
            except IndexError:  # If -s was never given
                arguments["Status"] = "Flag (-s) was used, but no argument was given."
                return arguments
        elif value.lower() == "-s" and already_sigma == True:
            arguments["Status"] = "Flag (-s) was used more than once."
            return arguments

        elif (
            value.lower() == "-i" and already_intensity == False
        ):  # Try to fetch the intensity value
            try:
                intensity = float(content_list[index + 1])
                if intensity > 15 or intensity < 0:
                    intensity = 0.1
                arguments["Intensity"] = intensity
                already_intensity = True
            except ValueError:  # If -i is not int
                arguments[
                    "Status"
                ] = "Invalid intensity (-i) argument given [argument must be a number]"
                return arguments
            except IndexError:  # If -i was never given
                arguments["Status"] = "Flag (-i) was used, but no argument was given."
                return arguments
        elif value.lower() == "-i" and already_intensity == True:
            arguments["Status"] = "Flag (-i) was used more than once."
            return arguments

        elif (
            value.lower() == "-nmd" and already_NMD == False
        ):  # Try to fetch the NMD value
            try:
                nmd = float(content_list[index + 1])
                if nmd > 10 or nmd < 1:
                    nmd = 1.0
                arguments["NMD"] = nmd
                already_NMD = True
            except ValueError:  # If -i is not int
                arguments[
                    "Status"
                ] = "Invalid NMD (-nmd) argument given [argument must be a number]"
                return arguments
            except IndexError:  # If -i was never given
                arguments["Status"] = "Flag (-nmd) was used, but no argument was given."
                return arguments
        elif value.lower() == "-nmd" and already_NMD == True:
            arguments["Status"] = "Flag (-nmd) was used more than once."
            return arguments

    # Final check to ensure nothing weird was fed through this command
    if any([already_NMD, already_intensity, already_sigma]) != True:
        arguments[
            "Status"
        ] = "Invalid arguments given. Arguments must be: <-s>, <-i>, <-nmd>. Arguments may be optional."
        logging.info(f"{already_sigma}, {already_intensity}, {already_NMD}")
    else:
        arguments["Status"] = ""

    logging.info(f"!tocoin : Processed {content} as {arguments}")
    return arguments


euro_country_list_fr = [
    "allemagne",
    "autriche",
    "belgique",
    "espagne",
    "finlande",
    "france",
    "irlande",
    "italie",
    "luxembourg",
    "pays-bas",
    "portugal",
    "grece",
    "slovenie",
    "chypre",
    "malte",
    "slovaquie",
    "estonie",
    "lettonie",
    "lituanie",
    "monaco",
    "saint-marin",
    "andorre",
    "croatie",
    "vatican",
]

types = ["1c", "2c", "5c", "10c", "20c", "50c", "1", "2", "2cc"]

blacklist = ["pattern", "Pattern"]

long_types = [
    "1 Euro Cent",
    "2 Euro Cent",
    "5 Euro Cent",
    "10 Euro Cent",
    "20 Euro Cent",
    "50 Euro Cent",
    "1 Euro",
    "2 Euro",
]


to_type = {
    "1c": "1 Euro Cent",
    "2c": "2 Euro Cent",
    "5c": "5 Euro Cent",
    "10c": "10 Euro Cent",
    "20c": "20 Euro Cent",
    "50c": "50 Euro Cent",
    "1": "1 Euro",
    "2": "2 Euro",
    "2cc": "2 Euro Commemorative",  # Beware of additional checks one might need to run!!!
}

from_type = {
    "1 cent": "1c",
    "2 cents": "2c",
    "5 cents": "5c",
    "10 cents": "10c",
    "20 cents": "20c",
    "50 cents": "50c",
    "1 euro": "1",
    "2 euro": "2",
    "2 euro commemorative": "2cc",
}

country_to_french = {
    "Andorra": "andorre",
    "Austria": "autriche",
    "Belgium": "belgique",
    "Croatia": "croatie",
    "Cyprus": "chypre",
    "Estonia": "estonie",
    "Finland": "finlande",
    "France": "france",
    "Germany": "allemagne",
    "Greece": "grece",
    "Ireland": "irlande",
    "Italy": "italie",
    "Latvia": "lettonie",
    "Lithuania": "lituanie",
    "Luxembourg": "luxembourg",
    "Malta": "malte",
    "Monaco": "monaco",
    "Netherlands": "pays-bas",
    "Portugal": "portugal",
    "San Marino": "saint-marin",
    "Slovakia": "slovaquie",
    "Slovenia": "slovenie",
    "Spain": "espagne",
    "Vatican": "vatican",
}


country_id_to_french = {
    "de": "allemagne",
    "at": "autriche",
    "be": "belgique",
    "es": "espagne",
    "fi": "finlande",
    "fr": "france",
    "ie": "irlande",
    "it": "italie",
    "lu": "luxembourg",
    "nl": "pays-bas",
    "pt": "portugal",
    "gr": "grece",
    "si": "slovenie",
    "cy": "chypre",
    "mt": "malte",
    "sk": "slovaquie",
    "ee": "estonie",
    "lv": "lettonie",
    "lt": "lituanie",
    "mc": "monaco",
    "sm": "saint-marin",
    "ad": "andorre",
    "va": "vatican",
}

french_to_emoji = {
    "allemagne": "🇩🇪",
    "autriche": "🇦🇹",
    "belgique": "🇧🇪",
    "espagne": "🇪🇸",
    "finlande": "🇫🇮",
    "france": "🇫🇷",
    "irlande": "🇮🇪",
    "italie": "🇮🇹",
    "luxembourg": "🇱🇺",
    "pays-bas": "🇳🇱",
    "portugal": "🇵🇹",
    "grece": "🇬🇷",
    "slovenie": "🇸🇮",
    "chypre": "🇨🇾",
    "malte": "🇲🇹",
    "slovaquie": "🇸🇰",
    "estonie": "🇪🇪",
    "lettonie": "🇱🇻",
    "lituanie": "🇱🇹",
    "monaco": "🇲🇨",
    "saint-marin": "🇸🇲",
    "andorre": "🇦🇩",
    "vatican": "🇻🇦",
    "croatie": "🇭🇷",
}

french_to_genitive = {
    "allemagne": "German",
    "autriche": "Austrian",
    "belgique": "Belgian",
    "espagne": "Spanish",
    "finlande": "Finnish",
    "france": "French",
    "ireland": "Irish",
    "italie": "Italian",
    "luxembourg": "Luxembourgish",
    "pays-bas": "Dutch",
    "portugal": "Portuguese",
    "grece": "Greek",
    "slovenie": "Slovene",
    "chypre": "Cypriot",
    "malte": "Maltese",
    "slovaquie": "Slovak",
    "estonie": "Estonian",
    "lettonie": "Latvian",
    "lituanie": "Lithuanian",
    "irlande": "Irish",
    "monaco": "Monégasque",
    "saint-marin": "Sammarinese",
    "andorre": "Andorran",
    "vatican": "Vatican",
}


default_year = [i for i in range(1999, 2031)]
default_types = types

clean_msg = """In general, **you should never clean coins.** This is because most cleaning methods can remove tarnishing or luster on coins which naturally develops over time, and may also leave scratch marks on the coin. Even lightly polishing it with a cloth may significantly impact a coins surface! To most collectors, this damage is noticeable and _significantly_ impacts the value of a coin.
    
The above advice is mostly meant towards older coins (usually pre-euro). Since euro coins are rarely worth a significant amount over face value (especially when found in circulation), cleaning them won't significantly lower their value. However, it is _still not recommended to clean them_ if you intend on trading coins or intend on your collection increasing in value in the future.
    
If your coins are physically dirty (i.e. due to dirt), __there are safe methods of removing it__. Soak the coin in distilled water or __100%__ acetone[see below], rinse with a fresh portion of the same liquid, and allow the coin to air-dry. When in doubt, feel free to ask members on the server for help!
    
*Use only pure acetone. Do not use acetone-containing products (i.e. nail polish remover). When using acetone, do not use plastic containers, and use it in a well-ventilated area. You can purchase pure acetone in most hardware stores.
"""

storage_msg_1 = """There are many safe methods of storing coins. The most common methods are to use 2x2 flips, capsules, or special albums. 
    
2x2 flips are small cardboard flips with holes cut in which are covered by film. You put the coin inside and fold the flips shut. Depending on the flip, the flip will either glue itself shut, or you will need to staple it shut. If you need to staple the flip shut, make sure that your stapler does not contact the coin inside the flip, otherwise it may leave a mark on the coin! Once inside the coin is protected from the outside environment. You still need to be careful with how you store your coins, though. There are special albums which can store 2x2 flips. The downside is that the flips can be quite big and you will need a lot of album space to store them. Lots of people also prefer to store flips in special boxes. There's lots of space on the flip to write information about the coin, or alternatively you can download flip tags made by chris24o1#9608 which you can glue onto coin flips here: https://discordapp.com/channels/555331630206681108/555333655866769418/930114755027402792
    
Capsules are small plastic covers which you can put your coin in. The advantage is that because they are hard surfaces, its less likely for the coin to be defaced by contact with another flip. The disadvantage is that they can be slightly more expensive and harder to store.
"""

storage_msg_2 = """There are many types of albums to store your coin in. __The only advice you need to follow is to ensure that the albums do not contain PVC.__ PVC is a chemical which leaves ugly green marks on a coin over time! PVC damage can be removed safely, but it is a nuisance to do so. It's best to avoid albums with the chemical for long-term storage.
    
Lighthouse/Leuchtturm is a very reliable brand for purchasing coin supplies. Your LCS should have a supply of storage materials for your coins. Alternatively, department stores are also a good place to check!
    
If you have any other questions about storing coins, feel free to inquire the community - we will be more than willing to help!"""

crh_info = """**What is Coin Roll Hunting?**
- __Coin Roll Hunting (CRH)__ is a hobby which many users on this server participate in regularly. The idea is to go to a bank, purchase coin rolls, then to look through the rolls for any special coins you don't have or may want to keep for trading. The regular coins you don't need anymore you deposit back into the bank. It's a cheap way to quickly expand your collection by only looking through circulated coins.

**How do I get started with Coin Roll Hunting?**    
- To get started with CRH, go to your local bank and ask to purchase coin rolls. In some banks, this process is even automated with machines. Sometimes you need to have a bank account with the bank, sometimes you don't, and sometimes purchasing rolls costs a little over face value. The exact process varies by country. To receive detailed information by country, select a country from the dropdown option below. 

**What do I do when I am done with the hunt?**   
- When you're done and you've looked through the rolls, you can go back and deposit your coins by using a coin counting machine. __It is generally not recommended to go back to the same branch you used to purchase the coins__, and to have separate branches dedicated to purchasing and depositing coins. Otherwise you run the risk of searching through rolls of coins you've already searched through. This depends on the country, however, as some banks may ship their deposited coins to a central coin wrapping place instead, and you wouldn't need to worry about depositing your coins in a different branch.
  
- Lastly, our community is very interested in live coin roll hunts! If you plan on hunting and don't mind livestreaming your hunt in a vc, don't hesitate to let people know in #coin-hunts!"""

rare_coins = """__Be sceptical of online listings of coins claiming that your coin is worth a lot of money.__ People like to put up listings for very common circulation coins claiming they are worth thousands, when in reality they are probably worth face value. There are many factors which go into what makes a coin rare, and it's best to do more research by looking into mintage figures and sold ebay listings. When in doubt, you can also ask the community in the #values channel to give their own opinion into the value of a coin.
    
__Greece 2002S is not a rare coin, nor is it a mintage error.__ In 2002, Greece could not make enough 2 euro coins for the introduction of the euro, so they asked Finland to help them out by minting some 2 euro coins for them. Finland made approximately __70 million__ 2 euro coins for Greece and marked them with an "S" mintmark (S for "Suomi"). This is the most common coin listed on marketplaces for extremely high prices. """

tocoin_help_menu = f"""___***COINDESIGNER HELP***___
With CoinDesigner, you can convert any coin design you want into a 2 euro coin! However, the command may be a bit tricky to figure out how to use.

First, create an image. The image should be square (otherwise itll be squished!) and ideally black and white. Lighter areas will stand out more in the final design.
Here are a few good example images you can use to test out the program: https://imgur.com/a/4PcuMoA

Next, select the image options by running the command ``/tocoin settings``. To reset to default settings run the command ``/tocoin default``.
<:emote:{emote_id}> ``sigma`` modifies how blurry (or sharp) the coin will appear to be. Higher ``sigma`` = more blurriness. 
<:emote:{emote_id}> ``intensity`` modifies how big the fields of the coin will be. Higher ``intensity`` = more noticeable fields.
<:emote:{emote_id}> ``nmd`` modifies how much dark areas of the coin pop out. Higher ``nmd`` = more noticeable dark areas. This is hard to tell, however, so it is recommended to keep this at 1.5 - 5.
Fool around with these numbers until you feel like the coin looks good enough!

To convert the image, select the message with the image, and go into message options (hold message on mobile, click on the three dots on PC) and go to Apps -> Convert. The bot will then post your converted coin in the chat! It may take a few seconds to do so.
"""

country_id_help_menu = """**TWO-LETTER COUNTRY IDENTIFICATION CODES**
AD = Andorra | AT = Austria | BE = Belgium | CY = Cyprus | DE = Germany | EE = Estonia | ES = Spain | FI = Finland | FR = France | GR = Greece | HR = Croatia
IE = Ireland | IT = Italy | LT = Lithuania | LU = Luxembourg | LV = Latvia | MC = Monaco | MT = Malta | NL = Netherlands | PT = Portugal | SI = Slovenia | 
SK = Slovakia | SM = San Marino | VA = Vatican 
"""

french_to_crhhelp = {
    "allemagne": """Coin roll availability may vary across banks and branches, as well as the price. You must be a customer to purchase.
**Sparkasse:** 50-150ct per roll.
**Volksbank:** 25ct per roll.
**Deutsche Post:** Free, get hand-rolled coins.
**Bundesbank:** Commemoratives can be exchanged for free as a customer, may be possible as foreigner. May swap 5, 10, and 20 euro for face value if available.""",
    "autriche": """Availability varies by bank.
**Bank Austria:** 20ct per roll. Can be purchased with cash at machines (available to everyone, but not in all branches, look for the filter option Münzrollengeber at https://filialen.bankaustria.at/de/).
**Erste Bank:** 10ct per roll. Must be a customer and pay with card at machines. Free when purchased at counters (but counters will redirect you to machines if they work), counters accept cash.
Depositing coins is free up to 100 euros/day, at which point you pay 1% for anything over 100 euros. You also must be a customer. 
**Raiffeisenbank:** 1 euro per roll if you aren't a customer, 30c per roll if you are. Depositing is free if you are a customer.
**Volksbank:** Reportedly free with no need of being a customer, needs to be confirmed 
**Austrian National Bank:** Does not distribute circulated rolls but sells CC rolls at face value on release as well as distributing UNC rolls for all denominations.
""",
    "belgique": """You can visit the European/Belgium central bank in Brussels as an EU citizen. You can order coin rolls for free, up to 2000 euros in value. (See https://www.youtube.com/watch?v=I4gwrpsl2Bk). They seem to distribute uncirculated, standard coins.
**KBC:** Free for customers, otherwise you must pay.
**Argenta:** €1.50 processing fee, but no limit on rolls.
There are no ATMs with coin rolls.""",
    "espagne": """Coin rolls are free for customers. Others can also get rolls at an unclear price.
**Bank of Spain:** Sells individual coins and CC rolls (even of other countries).
**BBVA:** Madrid: free of charge. Alicante: €2 for 5 rolls. Seems to vary by region.
**Banco Santander:** Free, must be customer.
**La Caixa:** Free, can use cash, no need to be customer""",
    "finlande": """No coin roll machines, but you can find vending machines or coin exchange machines (albeit they are rare).
**Aktia:** Free of charge.
**Bank of Finland:** Probably not possible.""",
    "france": """Coin roll machines are uncommon - only some banks have them and you need to be a customer. You may also need to order them in advance.
**CIC:** Free of charge (must be customer)
**Credit Agricole:**  Free of charge (must be customer)
**Caisse d'Épargne:** Free of charge (must be customer)
**Le Crédit Lyonnais (LCL):** Has coin roll machines but unknown if you need to be customer or if they charge money.""",
    "irlande": """Coin rolls available at banks with a fee of 1.00 per roll.
Could be free if you only need a few rolls.
Central Bank does not distribute any coins.""",
    "italie": """Information missing (feel free to contribute by letting bot devs know!)
**Bank of Italy:** Sells rolls to anyone.
**Banca Cambiano:** Has coin roll machines, but it is unknown if you need to be a customer or how much they charge.""",
    "luxembourg": """🇱🇺 Information missing (feel free to contribute by letting bot devs know!)
**Dexia-Bank:** You should be able to get coin rolls for free.
**BCL:** Unknown. Webshop sells commemoratives at face value, whether this is for sale in person is not known.""",
    "pays-bas": """Note that 1c and 2c coins are never used and hence unavailable in rolls.
**ING, Rabobank, and ABN AMRO:** You can get coin rolls from Geldmaat coin roll machines, which are placed in the Gamma or Karwei. Must be customer. (https://www.locatiewijzer.geldmaat.nl/?fiver&functionality=Munten%20opnemen) (See https://www.youtube.com/watch?v=AcfeTg05a70 for instructions)
**ABN AMRO:** 30ct per roll (min 10 rolls)
**ING:** 35ct per roll + 7 euro "service fee"
**Rabobank:** 50ct per roll + 7 euro "service fee"
The Dutch Central Bank does not distribute circulated rolls.
TIP: At stations, you may find "Smullers" which will sometimes have an exchange machine (useful for 10/20/50 cent rolls).""",
    "portugal": """May be incomplete (feel free to contribute by letting bot devs know!) 
**Banco de Portugal (Lisbon):** Free coin bags for everyone.
*8Millenium BCP:** Free coin bags (for customers).""",
    "grece": """May be incomplete (feel free to contribute by letting bot devs know!) 
Cannot buy coin rolls anywhere.
Getting coins from the bank is free for customers.
**Bank of Greece (Τράπεζα της Ελλάδος):** Free coin rolls for everyone (you need to show ID card), also latest €2 commemoratives are sold at face value.""",
    "slovenie": """May be incomplete (feel free to contribute by letting bot devs know!) 
**In general:** 1.20 per roll.
**Bank of Slovenia:** Sells commemorative coins for face value.
**Slovenian national bank:** Free coin rolls for everyone.""",
    "chypre": """Incomplete (feel free to contribute by letting bot devs know!)""",
    "malte": """Incomplete (feel free to contribute by letting bot devs know!) Generally hard to get coin rolls.
**BOV & HSCB Malta:** 30c per roll. Order coin rolls through their online platform (only for customers).""",
    "slovaquie": """May be incomplete (feel free to contribute by letting bot devs know!) 
**Tatra Banka:** 5 euros to buy an unlimited amount of rolls (must be customer).
May be able to get UNC rolls from the national bank. (someone inquire please)""",
    "estonie": """Difficult to obtain, sadly.
**All banks:** Coin rolls are very expansive, and you must make an appointment first (customers only)
**Central Bank of Estonia Museum (Tallinn):** Purchase CCs (even those released years ago) at _face value_ (also an interesting museum in general)""",
    "lettonie": """Incomplete (feel free to contribute by letting bot devs know!)
**In general:** 0.60c per roll.""",
    "lituanie": """No information available. (feel free to contribute by letting bot devs know!)""",
    "monaco": """No information available. (feel free to contribute by letting bot devs know!)""",
    "saint-marin": """No information available. (feel free to contribute by letting bot devs know!)""",
    "andorre": """No information available. (feel free to contribute by letting bot devs know!)""",
    "vatican": """Ask the Pope nicely and he'll probably give you some Vatican coins for free.""",
    "croatie": """No information available (feel free to contribute by letting bot devs know!)""",
}

help_text = f"""EuroBot is our discord bot and is intended to help collectors on this server with various tools. This is a list of all commands which are available to regular members. To access the help menu, run the command `/help`.

<:emote:{int(emote_id)}> **Information Commands:**
`/clean` - Displays information about cleaning coins
`/crh` - Displays information about coin roll hunting in the eurozone, as well as detailed information for each country.
`/info` - Displays server information and bot information.
`/rare` - Displays information about "rare" coins, and warns to take online listings of common coins with a grain of salt.
`/storage` - Displays information about how to store coins properly.

<:emote:{int(emote_id)}> **Search Commands:**
`/search help` - Displays information on how to use EuroBot's search function
`/search coin [country] {{year}} {{type}}` - Searches for a euro coin in the database
`/search id [id]` - Searches for a euro coin in the database by Numista ID
`/fsearch [query]` - "Fast search" for a coin in the database (usage described with the search help command)

<:emote:{int(emote_id)}> **CoinDesigner Commands:**
`/tocoin help` - Display information on how to use CoinDesigner
`/tocoin settings {{sigma}} {{intensity}} {{nmd}}` - Change CoinDesigner settings
`/tocoin reset` - Reset coindesigner settings

<:emote:{int(emote_id)}> **Other Commands:**
`/banknote {{serial}}` - Display information about a Euro Banknote with the specified serial number
`/demintmark {{year}}` - Display location of mintmark on a German CC minted in {{year}}"""

search_help = f"""

EuroBot's search functionality allows you to quickly search through Numista's database for all euro coins. Note that this only includes regular issue (i.e. 1c - 2 euro) coins, although it does include NIFC ones. EuroBot will also display the mintages for each coin.

<:emote:{int(emote_id)}> **Generic Search:**
`/search coin` is the command to execute a generic search. You will notice that there are three requirements - country, year, and type - of which only one (country) is mandatory. Additionally, the bot autocompletes a list of arguments you can include for each query. 

The search will yield a picture of the coin, some text describing the design, and mintage figures, as well as a direct link to the coin's Numista page. 

Sometimes the search yields multiple results. If that's the case, you can either use the buttons to select a result, or run the command `/search id [id] {{year}}` to select one via its numista ID. You can add {{year}} to narrow down the mintages if there are lots of them displayed.

<:emote:{int(emote_id)}> **Fast Search (fsearch):**
In a hurry? With `/fsearch [query]` you can execute a search much more quickly. The query consists of the required two letter TLD of the country (i.e. "de" for germany, "at" for austria, "si" for slovenia), the optional denomination (must be of the type "1c", "2c", "5c", "10c", "20c", "50c", "1", "2", "2cc", where those with "c" refer to cents, "1" and "2" refer to 1- and 2-euro coins, and "2cc" to 2-euro commemoratives), as well as the optional year. These arguments can be in any order.

For example, `/fsearch query: 10c at 2006` returns the mintage of the Austrian 10c coin in 2006, and `/fsearch query: ad 2cc` returns a list of all Andorran 2-euro commemoratives.

If you used EuroBot 1.0: `/fsearch` is used the exact same way as `eur!search`, except for the additional `query:` (which gets automatically added by discord)

<:emote:{int(emote_id)}> **Note about new coins:**
The database which EuroBot uses is remotely downloaded from Numista and requires updating sometimes by the developers. If you notice that a coin is missing, let the developers know.

"""
