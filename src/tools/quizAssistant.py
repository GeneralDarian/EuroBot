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

AN_Table = QuizType('Andorra', True, 'Quiz yourself on the mintages of Andorra!', ['andorra'])
AT_Table = QuizType('Austria', True, 'Quiz yourself on the mintages of Austria!', ['austria'])
BE_Table = QuizType('Belgium', True, 'Quiz yourself on the mintages of Belgium!', ['belgium'])
HR_Table = QuizType('Croatia', True, 'Quiz yourself on the mintages of Croatia!', ['croatia'])
CY_Table = QuizType('Cyprus', True, 'Quiz yourself on the mintages of Cyprus!', ['cyprus'])
EE_Table = QuizType('Cyprus', True, 'Quiz yourself on the mintages of Estonia!', ['estonia'])
FI_Table = QuizType('Cyprus', True, 'Quiz yourself on the mintages of Finland!', ['finland'])
EU_Table = QuizType('All Coins', True, 'Quiz yourself on the mintages of all EU countries!', ['andorra', 'austria', 'belgium', 'croatia', 'cyprus','estonia','finland'])

Design_Table = QuizType('Design', False, 'Quiz yourself on the individual euro coin designs!', ['design_trivia'])

QuizList = [
    AN_Table,
    AT_Table,
    BE_Table,
    HR_Table,
    CY_Table,
    EE_Table,
    FI_Table,
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