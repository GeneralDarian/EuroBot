Currently added commands. Note that any of the following prefixes can be used (by default): `eur!`, `Eur!`, `€`

## USER COMMANDS

- `eur!help`

  - Displays the help menu

- `eur!info`

  - Displays information about the server the bot is currently in, the number of people with the role with ID ``VERIFIED_TRADER_GROUP_ID``, days the server has existed, and bot information

- `eur!storage`

  - Informative command on how to store coins properly.

- `eur!rare`

  - Informative command on which coins are rare and what to look out for when looking up prices online.

- `eur!clean`

  - Informative command on cleaning coins.

- `eur!crh`

  - Informative command on how to do coin roll hunts (CRH).

- `eur!fotw`

  - Informative command on how FOTW works.

- `eur!search`

  - Looks through the database and searches for coins. There are two types of searches one can make: The first in the format ``eur!search <country> <denomination> <year>``, where ``<country>`` is either of the english form with no spaces (i.e. "Austria", "Sanmarino", etc.) or the two-letter country code (i.e. "AT", "SM"), ``<denomination>`` is of the form ``1c, 2c, 5c, 10c, 20c, 50c, 1, 2, 2cc``, and ``<year>`` is a year between 1999-2030. In this case, all three arguments can be in any order but you must include the country. If a search returns multiple results you can use ``eur!search ID <id> <year>`` to pick which result you want detailed info of. ``<id>`` must be included but ``<year>`` is optional, and this time all arguments must be in order. Here are a few example searches:
  - ``eur!search mc 2020`` - All coins from MONACO minted in 2020
  - ``eur!search 2c austria`` - All 2 cent coins from AUSTRIA
  - ``eur!search ad 10c 2016`` - 10 cents from ANDORRA minted in 2016
  - ``eur!search id 49385`` - Information about coin with numista id 49385 (Monaco 2013)

- `eur!banknote`

  - Get euro banknote information. Do ``eur!banknote <serialno>`` to enter a serial number and ``eur!banknote`` or ``eur!banknote help`` for help finding serial numbers.

- `eur!tocoin`

  - Turn a square black-and-white image into a 2 euro coin design, courtesy of [@joaoperfig](https://github.com/joaoperfig)'s [CoinDesigner](https://github.com/joaoperfig/CoinDesigner). With no arguments the command is the exact same as running ``eur!tocoin -s 0.1 -i 2.0 -nmd 1.5``. Play around with some of these numbers until you get better results. You can run the command by either uploading an image or replying to an already sent image.

## ADMIN ONLY COMMANDS

- `eur!refreshAPI`

  - Refreshes the API by requesting for all euro coins from all eurozone countries and saving them in /src/json_data. Not recommended to run this all the time since it uses a lot of API requests.

- `eur!getWinners`

  - Gets the winners for this week's find of the week competition and resets the current competition.
