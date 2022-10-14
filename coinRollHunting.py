import time

class coinRollHunt:
    def __init__(self, user_id: str, hunt_time: str, img: str, msg_id: str):
        self.user_id = user_id
        self.hunt_time = hunt_time
        self.img = img
        self.msg_id = msg_id
        if int(hunt_time) < time.time():
            raise ValueError(f'The specified time is in the past.')


french_to_crhhelp = {'allemagne': """Coin roll availability may vary across banks and branches, as well as the price. You must be a customer to purchase.
Sparkasse: 50-150ct per roll.
Volksbank: 25ct per roll.
Deutsche Post: Free, get hand-rolled coins.
Bundesbank: Commemoratives can be exchanged for free as a customer, may be possible as foreigner. May swap 5, 10, and 20 euro for face value if available.""",


                   'autriche': """Bank Austria: 20ct per roll. Can be purchased with cash at machines (available to everyone, but not in all branches, look for the filter option Münzrollengeber at https://filialen.bankaustria.at/de/).
Erste Bank: 10ct per roll. Must be a customer and pay with card at machines. Free when purchased at counters (but counters will redirect you to machines if they work), counters accept cash.
Depositing coins is free up to 100 euros/day, at which point you pay 1% for anything over 100 euros. You also must be a customer. 
Raiffeisenbank: Possible to get coin rolls for free, even if you aren't a customer. 
Austrian National Bank: Does not distribute circulated rolls but sells CC rolls at face value on release.
                   """,


                   'belgique': """You can visit the European/Belgium central bank in Brussels as an EU citizen. You can order coin rolls for free, up to 2000 euros in value. (See https://www.youtube.com/watch?v=I4gwrpsl2Bk). They seem to distribute uncirculated, standard coins.
KBC: Free for customers, otherwise you must pay.
Argenta: €1.50 processing fee, but no limit on rolls.
No ATMs with coin rolls.""",


                   'espagne': """Coin rolls are free for customers. Others can also get rolls at an unclear price.
Bank of Spain sells individual coins and CC rolls (even of other countries).
BBVA: Madrid: free of charge. Alicante: €2 for 5 rolls. Seems to vary by region.
Banco Santander: Free, must be customer.""",


                   'finlande': """No coin roll machines, but you can find vending machines or coin exchange machines (albeit they are rare).
Aktia: Free of charge.
Bank of Finland: Probably not possible.""",


                   'france': """Coin roll machines are rare. Only some banks have them and you need to be a customer. You may also need to order them in advance.
CIC: Free of charge (must be customer)
Credit Agricole:  Free of charge (must be customer)
Caisse D'épargne: Free of charge (must be customer)""",


                   'ireland': """Coin rolls available at banks with a fee of 1.00 per roll.
Could be free if you only need a few rolls.
Central Bank does not distribute any coins.""",


                   'italie': 'Bank of Italy sells rolls to anyone.',


                   'luxembourg': 'At Dexia-Bank you should be able to get coin rolls for free.',


                   'pays-bas': """Note that 1c and 2c coins are never used and hence unavailable in rolls.
As a customer of ING, Rabobank or ABN AMRO, you can get coin rolls from Geldmaat coin roll machines, which are placed in the Gamma or Karwei. (https://www.locatiewijzer.geldmaat.nl/?fiver&functionality=Munten%20opnemen) (See https://www.youtube.com/watch?v=AcfeTg05a70 for instructions)
ABN AMRO: 30ct per roll (min 10 rolls)
ING: 35ct per roll + 7 euro "service fee"
Rabobank: 50ct per roll + 7 euro "service fee"
The Dutch Central Bank does not distribute circulated rolls.
TIP: At stations, you may find "Smullers" which will sometimes have an exchange machine (useful for 10/20/50 cent rolls).""",


                   'portugal': """Banco de Portugal (Lisbon): Free coin bags for everyone.
Millenium BCP: Free coin bags (for customers).""",


                   'grece': """Cannot buy coin rolls anywhere.
Getting coins from the bank is free for customers.
National bank of Greece: Free coin rolls for everyone (you need to show ID card), also latest €2 commemoratives are sold at face value.""",


                   'slovenie': """1.20 per roll.
Bank of Slovenia sells commemorative coins for face value.
Slovenian national bank: Free coin rolls for everyone.""",


                   'chypre': """No information given.""",


                   'malte': """Generally hard to get coin rolls.
BOV & HSCB Malta: 30c per roll. Order coin rolls through their online platform (only for customers).""",


                   'slovaquie': """Tatra Banka: 20c per roll (only for customers).""",


                   'estonie': """All banks: Coin rolls are very expansive, and you must make an appointment first (customers only)
Central Bank of Estonia Museum (Tallinn): Purchase CCs (even those released years ago) at _face value_ (also an interesting museum in general)""",


                   'lettonie': """0.60c per roll.""",


                   'lituanie': """No information available.""",


                   'monaco': """No information available.""",


                   'saint-marin': """No information available.""",


                   'andorre': """No information available.""",


                   'vatican': """Ask the Pope nicely and he'll probably give you some Vatican coins for free."""}






