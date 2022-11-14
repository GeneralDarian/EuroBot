import time


class coinRollHunt:
    def __init__(self, user_id: str, hunt_time: str, img: str, msg_id: str):
        self.user_id = user_id
        self.hunt_time = hunt_time
        self.img = img
        self.msg_id = msg_id
        if int(hunt_time) < time.time():
            raise ValueError(f"The specified time is in the past.")


french_to_crhhelp = {
    "allemagne": """🇩🇪 Coin roll availability may vary across banks and branches, as well as the price. You must be a customer to purchase.
**Sparkasse:** 50-150ct per roll.
**Volksbank:** 25ct per roll.
**Deutsche Post:** Free, get hand-rolled coins.
**Bundesbank:** Commemoratives can be exchanged for free as a customer, may be possible as foreigner. May swap 5, 10, and 20 euro for face value if available.""",
    "autriche": """🇦🇹 Availability varies by bank.
**Bank Austria:** 20ct per roll. Can be purchased with cash at machines (available to everyone, but not in all branches, look for the filter option Münzrollengeber at https://filialen.bankaustria.at/de/).
**Erste Bank:** 10ct per roll. Must be a customer and pay with card at machines. Free when purchased at counters (but counters will redirect you to machines if they work), counters accept cash.
**Depositing coins is free up to 100 euros/day, at which point you pay 1% for anything over 100 euros. You also must be a customer. 
**Raiffeisenbank:** 1 euro per roll if you aren't a customer, 30c per roll if you are. Depositing is free if you are a customer.
**Volksbank:** Reportedly free with no need of being a customer, needs to be confirmed 
**Austrian National Bank:** Does not distribute circulated rolls but sells CC rolls at face value on release as well as distributing UNC rolls for all denominations.
""",
    "belgique": """🇧🇪 You can visit the European/Belgium central bank in Brussels as an EU citizen. You can order coin rolls for free, up to 2000 euros in value. (See https://www.youtube.com/watch?v=I4gwrpsl2Bk). They seem to distribute uncirculated, standard coins.
**KBC:** Free for customers, otherwise you must pay.
**Argenta:** €1.50 processing fee, but no limit on rolls.
There are no ATMs with coin rolls.""",
    "espagne": """🇪🇸 Coin rolls are free for customers. Others can also get rolls at an unclear price.
**Bank of Spain:** Sells individual coins and CC rolls (even of other countries).
**BBVA:** Madrid: free of charge. Alicante: €2 for 5 rolls. Seems to vary by region.
**Banco Santander:** Free, must be customer.
**La Caixa:** Free, can use cash, no need to be customer""",
    "finlande": """🇫🇮 No coin roll machines, but you can find vending machines or coin exchange machines (albeit they are rare).
**Aktia:** Free of charge.
**Bank of Finland:** Probably not possible.""",
    "france": """🇫🇷 Coin roll machines are uncommon - only some banks have them and you need to be a customer. You may also need to order them in advance.
**CIC:** Free of charge (must be customer)
**Credit Agricole:**  Free of charge (must be customer)
**Caisse d'Épargne:** Free of charge (must be customer)
**Le Crédit Lyonnais (LCL):** Has coin roll machines but unknown if you need to be customer or if they charge money.""",
    "ireland": """🇮🇪 Coin rolls available at banks with a fee of 1.00 per roll.
Could be free if you only need a few rolls.
Central Bank does not distribute any coins.""",
    "italie": """🇮🇹 Information missing (feel free to contribute by letting bot devs know!)
**Bank of Italy:** Sells rolls to anyone.
**Banca Cambiano:** Has coin roll machines, but it is unknown if you need to be a customer or how much they charge.""",
    "luxembourg": """🇱🇺 Information missing (feel free to contribute by letting bot devs know!)
**Dexia-Bank:** You should be able to get coin rolls for free.
**BCL:** Unknown. Webshop sells commemoratives at face value, whether this is for sale in person is not known.""",
    "pays-bas": """🇳🇱 Note that 1c and 2c coins are never used and hence unavailable in rolls.
**ING, Rabobank, and ABN AMRO:** You can get coin rolls from Geldmaat coin roll machines, which are placed in the Gamma or Karwei. Must be customer. (https://www.locatiewijzer.geldmaat.nl/?fiver&functionality=Munten%20opnemen) (See https://www.youtube.com/watch?v=AcfeTg05a70 for instructions)
**ABN AMRO:** 30ct per roll (min 10 rolls)
**ING:** 35ct per roll + 7 euro "service fee"
**Rabobank:** 50ct per roll + 7 euro "service fee"
The Dutch Central Bank does not distribute circulated rolls.
TIP: At stations, you may find "Smullers" which will sometimes have an exchange machine (useful for 10/20/50 cent rolls).""",
    "portugal": """🇵🇹 May be incomplete (feel free to contribute by letting bot devs know!) 
**Banco de Portugal (Lisbon):** Free coin bags for everyone.
*8Millenium BCP:** Free coin bags (for customers).""",
    "grece": """🇬🇷 May be incomplete (feel free to contribute by letting bot devs know!) 
Cannot buy coin rolls anywhere.
Getting coins from the bank is free for customers.
**Bank of Greece (Τράπεζα της Ελλάδος):** Free coin rolls for everyone (you need to show ID card), also latest €2 commemoratives are sold at face value.""",
    "slovenie": """🇸🇮 May be incomplete (feel free to contribute by letting bot devs know!) 
**In general:** 1.20 per roll.
**Bank of Slovenia:** Sells commemorative coins for face value.
**Slovenian national bank:** Free coin rolls for everyone.""",
    "chypre": """🇨🇾 Incomplete (feel free to contribute by letting bot devs know!)""",
    "malte": """🇲🇹 Incomplete (feel free to contribute by letting bot devs know!) Generally hard to get coin rolls.
**BOV & HSCB Malta:** 30c per roll. Order coin rolls through their online platform (only for customers).""",
    "slovaquie": """🇸🇰 May be incomplete (feel free to contribute by letting bot devs know!) 
**Tatra Banka:** 5 euros to buy an unlimited amount of rolls (must be customer).
May be able to get UNC rolls from the national bank. (someone inquire please)""",
    "estonie": """🇪🇪 Difficult to obtain, sadly.
**All banks:** Coin rolls are very expansive, and you must make an appointment first (customers only)
**Central Bank of Estonia Museum (Tallinn):** Purchase CCs (even those released years ago) at _face value_ (also an interesting museum in general)""",
    "lettonie": """🇱🇻 Incomplete (feel free to contribute by letting bot devs know!)
**In general:** 0.60c per roll.""",
    "lituanie": """🇱🇹 No information available. (feel free to contribute by letting bot devs know!)""",
    "monaco": """🇲🇨 No information available. (feel free to contribute by letting bot devs know!)""",
    "saint-marin": """🇸🇲 No information available. (feel free to contribute by letting bot devs know!)""",
    "andorre": """🇦🇩 No information available. (feel free to contribute by letting bot devs know!)""",
    "vatican": """🇻🇦 Ask the Pope nicely and he'll probably give you some Vatican coins for free.""",
}
