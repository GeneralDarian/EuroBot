import random
from math import ceil

class QuizType:
    def __init__(self, name: str, mintage: bool, desc: str, database_name: list[str]):
        """name: name of the quiz to be displayed
        mintage: is this a mintage-based quiz (True) or theory-based quiz (False)?
        desc: description of the quiz
        database_name: The name(s) of the database to pull the questions from (in Quiz.db)"""
        self.name = name
        self.mintage = mintage
        self.desc = desc
        self.database_name = database_name

AN_Table = QuizType('Andorra', True, '🇦🇩 Quiz yourself on the mintages of Andorra!\n', ['andorra'])
AT_Table = QuizType('Austria', True, '🇦🇹 Quiz yourself on the mintages of Austria!\n', ['austria'])
BE_Table = QuizType('Belgium', True, '🇧🇪 Quiz yourself on the mintages of Belgium!\n', ['belgium'])
HR_Table = QuizType('Croatia', True, '🇭🇷 Quiz yourself on the mintages of Croatia!\n', ['croatia'])
CY_Table = QuizType('Cyprus', True, '🇨🇾 Quiz yourself on the mintages of Cyprus!\n', ['cyprus'])
EE_Table = QuizType('Estonia', True, '🇪🇪 Quiz yourself on the mintages of Estonia!\n', ['estonia'])
FI_Table = QuizType('Finland', True, '🇫🇮 Quiz yourself on the mintages of Finland!\n', ['finland'])
FR_Table = QuizType('France', True, '🇫🇷 Quiz yourself on the mintages of France!\n', ['france'])
DE_Table = QuizType('Germany', True, '🇩🇪 Quiz yourself on the mintages of Germany!\n', ['germany_a', 'germany_d', 'germany_f', 'germany_g', 'germany_j'])
GR_Table = QuizType('Greece', True, '🇬🇷 Quiz yourself on the mintages of Greece!\n', ['greece'])
IE_Table = QuizType('Ireland', True, '🇮🇪 Quiz yourself on the mintages of Ireland!\n', ['ireland'])
IT_Table = QuizType('Italy', True, '🇮🇹 Quiz yourself on the mintages of Italy!\n', ['italy'])
LV_Table = QuizType('Latvia', True, '🇱🇻 Quiz yourself on the mintages of Latvia!\n', ['latvia'])
LT_Table = QuizType('Lithuania', True, '🇱🇹 Quiz yourself on the mintages of Lithuania!\n', ['lithuania'])
LU_Table = QuizType('Luxembourg', True, '🇱🇺 Quiz yourself on the mintages of Luxembourg!\n', ['luxembourg'])
MT_Table = QuizType('Malta', True, '🇲🇹 Quiz yourself on the mintages of Malta!\n', ['malta'])
MC_Table = QuizType('Monaco', True, '🇲🇨 Quiz yourself on the mintages of Monaco!\n', ['monaco'])
NL_Table = QuizType('Netherlands', True, '🇳🇱 Quiz yourself on the mintages of the Netherlands!\n', ['netherlands'])
PT_Table = QuizType('Portugal', True, '🇵🇹 Quiz yourself on the mintages of Portugal!\n', ['portugal'])
SM_Table = QuizType('San Marino', True, '🇸🇲 Quiz yourself on the mintages of San Marino!\n', ['san_marino'])
SK_Table = QuizType('Slovakia', True, '🇸🇰 Quiz yourself on the mintages of Slovakia!\n', ['slovakia'])
EU_Table = QuizType('All Coins', True, '🇪🇺 Quiz yourself on the mintages of all EU countries!\n', [
    'andorra',
    'austria',
    'belgium',
    'croatia',
    'cyprus',
    'estonia',
    'finland',
    'france',
    'germany_a',
    'germany_d',
    'germany_f',
    'germany_g',
    'germany_j',
    'greece',
    'ireland',
    'italy',
    'latvia',
    'lithuania',
    'luxembourg',
    'malta',
    'monaco',
    'luxembourg',
    'netherlands',
    'portugal',
    'san_marino',
    'slovakia'
])

Design_Table = QuizType('Design', False, 'Quiz yourself on the individual euro coin designs!', ['design_trivia'])

QuizList = [
    AN_Table,
    AT_Table,
    BE_Table,
    HR_Table,
    CY_Table,
    EE_Table,
    FI_Table,
    FR_Table,
    DE_Table,
    GR_Table,
    IT_Table,
    IE_Table,
    LV_Table,
    LT_Table,
    LU_Table,
    MT_Table,
    MC_Table,
    NL_Table,
    PT_Table,
    SM_Table,
    SK_Table,
    EU_Table,
    Design_Table
]





def generateoptions(mintage: str) -> dict:
    """Generates a list of viable mintages"""
    max = "5000000"  # max should be 5 mil but if you want to change that for some reason here you go
    correct_ans = mintage

    # if mintage is 5M/NIFC:
    # - correct ans should be 5M/NIFC (so that the program knows how to assemble the return)
    # - mintage should STILL be generated in order to get 4 options
    # - program should know to generate one more option (hence options_to_generate = 4)
    if mintage.lower() == "5m or higher":
        mintage = str(random.randint(10, 2500)) + "000"
        options_to_generate = 4
    elif mintage.lower() == "nifc":
        mintage = str(random.randint(10, 2500)) + "000"
        options_to_generate = 4
    else:
        options_to_generate = 3

    # process for generating random answers
    # pointer: how many numbers to generate
    # zeroes: how many zeroes to stick afterwards
    for ind, val in enumerate(mintage[::-1]):
        if val != "0":
            pointer = len(mintage) - ind
            zeroes = ind
            break

    if pointer < 2:  # pointer should be at least 2 digits long so that if, say,
        # "1,000,000" is submitted then itll be reported as "10" and not "1"
        # (which would lead to complications due to buffer)
        pointer = 2

    # max[:0] = ''
    # to prevent int('') from throwing an error
    # it makes sure zeroes != 0, and if it is, then use int(max)
    if zeroes != 0:
        max_pointer = int(max[:-1 * zeroes])
    else:
        max_pointer = int(max)

    buffer = int(str(max_pointer)[:-1])  # how spaced apart should the options be? this is 250,000
    opt_list = []

    # generate all options
    while True:
        rand = random.randint(0, max_pointer)

        for num in opt_list:
            if abs(num - rand) < buffer:
                break
        else:
            opt_list.append(rand)

        if len(opt_list) >= options_to_generate:
            break

    for ind, val in enumerate(opt_list):
        # lol this looks stupid
        drop = random.random()
        if drop > 0.95 and zeroes >= 2:
            opt_list[ind] = f"{int(str(val) + (zeroes - 2) * '0'):,}"
        elif drop > 0.85 and zeroes >= 1:
            opt_list[ind] = f"{int(str(val) + (zeroes - 1) * '0'):,}"
        else:
            opt_list[ind] = f"{int(str(val) + zeroes * '0'):,}"

    return opt_list