from os import path
import logging
import sqlite3
from sqlite3 import Error
import random
from datetime import datetime

import discord
from discord import bot
from discord.commands import option
from discord.ext import commands
from tools import quizAssistant


def fetch_answer(db, id):
    """ create a database connection to a SQLite database """
    conn = None
    db_file = "data/Quiz.db"
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        print("Success at connection!")
        cur = conn.cursor()
    """db = database
    id = id of question"""
    print(f"SELECT correct_ans FROM {db} WHERE question_id = {id};")
    cur.execute(f"SELECT correct_ans FROM {db} WHERE question_id = {id};")
    rows = cur.fetchall()[0]
    conn.close()
    return rows[0]

def fetch_question(db):
    """Fetch a random question from database db"""
    conn = None
    db_file = "data/Quiz.db"
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    finally:
        cur = conn.cursor()
    """db = database
    id = id of question"""
    cur.execute(f"SELECT * FROM {db} ORDER BY RANDOM() LIMIT 1;")
    rows = cur.fetchall()[0]
    conn.close()
    return rows

async def ask_question(data: dict, channel: discord.TextChannel):
    """Asks a question in channel.
    channel MUST be a discord.TextChannel option
    data must be structured as follows:
    data['quiz_class']: The quiz class
    data['database']: Name of database
    data['id']: Question ID
    data['question']: The question title
    data['correct_answer']: The question's correct answer
    data[0]: Option one of the question
    data[1]: Option two of the question
    data[2]: Option three of the question
    data[3]: Option four of the question
    data[4]: Option five of the question
    data['mintage']: bool. True if this is a mintage-question (changes how answers are shuffled)
    data['image']: The image to display with the question
    data['label_option']: TRUE if you want buttons to be labelled with data[n], FALSE if you want them labeled 'OPTION N'"""

    #determine answer list and get position of correct answer
    ans_list = [] #this will become the list of answers in order (i.e. ans_list[0] = option 1, etc.)



    random.shuffle(ans_list)

    if data['mintage'] is True and str(data['correct_answer']).lower() == '5m or higher':
        correct_ans_index = (-1, 0)
    elif data['mintage'] is True and str(data['correct_answer']).lower() == 'nifc':
        correct_ans_index = (-1, 5)
    elif data['mintage'] is True:
        leeway = 20000
        if abs(data['correct_answer'] - 5000000) < leeway:
            correct_ans_index = (0,1)
        elif data['correct_answer'] > 5000000:
            correct_ans_index = (-1, 0)
        elif abs(data['correct_answer'] - 2000000) < leeway:
            correct_ans_index = (1, 2)
        elif data['correct_answer'] > 2000000:
            correct_ans_index = (-1, 1)
        elif abs(data['correct_answer'] - 1000000) < leeway:
            correct_ans_index = (2, 3)
        elif data['correct_answer'] > 1000000:
            correct_ans_index = (-1, 2)
        elif abs(data['correct_answer'] - 500000) < leeway:
            correct_ans_index = (3, 4)
        elif data['correct_answer'] > 500000:
            correct_ans_index = (-1, 3)
        else:
            correct_ans_index = (-1, 4)

    else:
        for n in range(4):
            try:
                if data[n] is not None:
                    ans_list.append(data[n])
                else:
                    break
            except KeyError:
                break
        random.shuffle(ans_list)
        correct_ans_index = (random.randint(0, len(ans_list) - 1))
        temp = ans_list[correct_ans_index]
        ans_list[correct_ans_index] = data['correct_answer']
        ans_list.append(temp)
        correct_ans_index = (-1, correct_ans_index)

    if data['mintage'] is True:
        ans_list.append("5 mil or higher")  # index 0
        ans_list.append("2 mil to 5 mil")  # index 1
        ans_list.append("1 mil to 2 mil")  # index 2
        ans_list.append("500k to 1 mil")  # index 3
        ans_list.append("Below 500k")  # index 4
        ans_list.append("NIFC")  # index 5

    #make embed and views (buttons)
    view = discord.ui.View(timeout=20, disable_on_timeout=True)
    embed = discord.Embed(
        title=data['question'],
        color=0xFFCC00,
    )
    embed.set_image(url=data['image'])

    for ind, val in enumerate(ans_list):
        if data['mintage'] is False:
            embed.add_field(name=f"OPTION {ind+1}", value=val, inline=False)

        #determine label
        if data['label_option'] is True:
            label = val
        else:
            label = f"OPTION {ind+1}"

        #add buttons
        if ind in correct_ans_index:
            print(f"Correct answer is: {label}")
            view.add_item(
                QuizButtons(option=label, correct=True, question_id=data['id'], database=data['database'], quiz=data['quiz_class'])
            )
        else:
            view.add_item(
                QuizButtons(option=label, correct=False, question_id=data['id'], database=data['database'], quiz=data['quiz_class'])
            )

    #send that shit
    await channel.send(embed=embed,view=view)

async def mintage_question(channel: discord.TextChannel, quiz: quizAssistant.QuizType):
    """Sorts out the dictionary which gets sent to ask_question when it is a MINTAGE-BASED question.
    channel: the channel to send to
    database: the database which the bot uses to ask for the correct answer to the question."""
    #0 = id, 1 = country (unused), 2 = deno, 3 = year, 4 = mintage, 5 = yearend, 6 = image
    #structure: What is the mintage of {database.capitalize()} {deno} {year}?

    #get database
    database = random.choice(quiz.database_name)

    rows = fetch_question(database)
    data = {}

    #get year
    if rows[5] is not None:
        year = random.randint(rows[3], rows[5])
    else:
        year = rows[3]

    #get deno
    if rows[2] == "1":
        deno = "1 euro"
    elif rows[2] == "2":
        deno = "2 euro"
    else:
        deno = rows[2]

    if rows[4].lower() == "5m":
        data['correct_answer'] = "5M or higher"
    elif rows[4].lower() == "nifc":
        data['correct_answer'] = "NIFC"
    else:
        data['correct_answer'] = int(rows[4])

    data['database'] = database
    data['question'] = f"What is the mintage of {database.capitalize()} {deno} {year}?"
    data['mintage'] = True
    data['image'] = rows[6]
    data['id'] = rows[0]
    data['label_option'] = True
    data['quiz_class'] = quiz



    print(data)
    await ask_question(data, channel)
    return

async def theory_question(channel: discord.TextChannel, quiz: quizAssistant.QuizType):
    """Sorts out the dictionary which gets sent to ask_question when it is a THEORY-BASED question.
    channel: the channel to send to
    database: the database which the bot uses to ask for the correct answer to the question."""
    # get database
    database = random.choice(quiz.database_name)

    rows = fetch_question(database)
    data = {}
    data['database'] = 'design_trivia'
    data['question'] = f"[DT#{rows[0]}] {rows[1]}"
    data['correct_answer'] = rows[2]
    data['quiz_class'] = quiz

    for n in range(4):
        if rows[n + 3] is not None and rows[n + 3] != '':
            data[n] = rows[n + 3]
        else:
            data[n] = None

    data['mintage'] = False
    data['image'] = rows[7]
    data['label_option'] = False
    data['id'] = rows[0]

    await ask_question(data=data, channel=channel)
    return

async def quiz_handler(channel: discord.TextChannel, quiz: quizAssistant.QuizType):
    if quiz.mintage is False:
        await theory_question(channel, quiz)
    else:
        await mintage_question(channel, quiz)


class NextContinueButton(discord.ui.Button):
    """Button which shows when you get a question right/wrong and continues the quiz"""
    def __init__(self, quiz: quizAssistant.QuizType, theory: bool):
        """Database: database to pull the question from
        theory: is this a theory based question? (true if yes)"""
        super().__init__(
            label="New question!",
            style=discord.ButtonStyle.success
        )
        self.quiz = quiz
        self.theory = theory

    async def callback(self, interaction: discord.Interaction):
        if self.theory is True:
            await theory_question(interaction.channel, self.quiz)
            await interaction.message.edit(view=None)
        else:
            await mintage_question(interaction.channel, self.quiz)
            await interaction.message.edit(view=None)

class NextCancelButton(discord.ui.Button):
    """Button which shows when you get a question right/wrong and cancels the quiz"""
    def __init__(self):
        super().__init__(
            label="Cancel Quiz",
            style=discord.ButtonStyle.danger
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message("Quiz has been cancelled.")
        await interaction.message.edit(view=None)

class QuizButtons(discord.ui.Button):
    def __init__(self, option, correct, question_id,  quiz: quizAssistant.QuizType, database: str):
        """If the answer is correct, then correct should be True.
        If the answer is not correct, then correct should correspond to the question ID.
        Database must be the name of the database which the question was taken from."""
        super().__init__(
            label=option,
            style=discord.ButtonStyle.primary
        )
        self.correct = correct
        self.quiz = quiz
        self.database = database
        self.question_id = question_id

    async def callback(self, interaction: discord.Interaction):
        desc_embed = fetch_answer(db=self.database, id=self.question_id)
        if self.quiz.mintage is True: #report the mintage if the quiz is mintage-based
            if desc_embed.lower() == "nifc":
                desc_embed = "The coin is NIFC"
            elif desc_embed.lower() == "5m":
                desc_embed = "Mintage: 5M or higher"
            else:
                desc_embed = f"Mintage: {int(desc_embed):,}"

        if self.correct is True:
            embed = discord.Embed(
                title=f"Correct Answer! [#{self.question_id}]",
                description=desc_embed,
                color=0x00CC00
            )
        else:
            embed = discord.Embed(
                title = f"Incorrect! [#{self.question_id}]",
                description=f"The correct answer is: {desc_embed}",
                color=0xFF0000
            )
        view = discord.ui.View(timeout=20, disable_on_timeout=True)
        view.add_item(
            NextContinueButton(theory=False, quiz=self.quiz)
        )
        view.add_item(
            NextCancelButton()
        )
        await interaction.response.send_message(embed=embed,view=view)

        await interaction.message.edit(view=None)




class Quiz(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(
            f"Cog {path.basename(__file__).removesuffix('.py')} loaded successfully"
        )


    @bot.command(description="Start a quiz!")
    @option(
        "type",
        description="The type of quiz to start. To get a list run this command without this argument.",
        required=False,
    )
    async def quiz(self, ctx, type):
        if type is None:
            desc_theory = "__**Theory-based quizzes**__"
            desc_mintage = "__**Mintage-based quizzes**__"
            for quiz_class in quizAssistant.QuizList:
                if quiz_class.mintage is False:
                    desc_theory += f"\n**{quiz_class.name}**\n{quiz_class.desc}"
                else:
                    desc_mintage += f"\n**{quiz_class.name}**\n{quiz_class.desc}"
            desc_theory += f"\n\n{desc_mintage}"
            embed=discord.Embed(
                title="EuroBot Quizzes",
                description=desc_theory,
                color=0xFFCC00
            )
            await ctx.respond(embed=embed)
        else:
            for quiz_class in quizAssistant.QuizList:
                if quiz_class.name == type.title():
                    quiz_type = quiz_class
                    break
            else:
                await ctx.respond("Error: The quiz type does not exist! Type ``/quiz`` for a list of quizzes.")
                return

            await ctx.respond("Starting quiz...!")
            await quiz_handler(channel=ctx.interaction.channel, quiz=quiz_type)
            return
            #have fun broski



def setup(client):
    client.add_cog(Quiz(client))