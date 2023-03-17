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
    db = "design_trivia"
    cur.execute(f"SELECT correct_ans FROM {db} WHERE question_id = {id};")
    rows = cur.fetchall()[0]
    conn.close()
    return rows[0]

class QuizButtons(discord.ui.Button):
    def __init__(self, option, correct, question_id, database):
        """If the answer is correct, then correct should be True.
        If the answer is not correct, then correct should correspond to the question ID.
        Database must be the name of the database which the question was taken from."""
        super().__init__(
            label=option,
            style=discord.ButtonStyle.primary
        )
        self.correct = correct
        self.database = database
        self.question_id = question_id

    async def callback(self, interaction: discord.Interaction):
        if self.correct is True:
            embed = discord.Embed(
                title=f"Correct Answer! [#{self.question_id}]",
                description=fetch_answer(db=self.database, id=self.question_id),
                color=0x00CC00
            )
        else:
            embed = discord.Embed(
                title = f"Incorrect! [#{self.question_id}]",
                description=f"The correct answer is: {fetch_answer(db=self.database, id=self.question_id)}",
                color=0xFF0000
            )
        await interaction.response.send_message(embed=embed)

        await interaction.message.edit(view=None)




class Quiz(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(
            f"Cog {path.basename(__file__).removesuffix('.py')} loaded successfully"
        )
        self.create_connection(r"data\Quiz.db")

    def create_connection(self, db_file):
        """ create a database connection to a SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            print(sqlite3.version)
        except Error as e:
            print(e)
        finally:
            print("Success at connection!")
            self.cur = conn.cursor()

    def fetch_answer(self, db, id):
        """db = database
        id = id of question"""
        db = "design_trivia"
        self.cur.execute(f"SELECT correct_ans FROM {db} WHERE question = {id};")
        rows = self.cur.fetchall()[0]
        return rows[0]


    @bot.command(description="Start a quiz!")
    async def askquestion(self, ctx):
        self.cur.execute("SELECT * FROM design_trivia ORDER BY RANDOM() LIMIT 1;")
        rows = self.cur.fetchall()[0]


        id = rows[0]
        questdesc = rows[1]
        correct_ans = rows[2]
        ot_ans_1 = rows[3]
        ot_ans_2 = rows[4]
        ot_ans_3 = rows[5]
        ot_ans_4 = rows[6]
        img = rows[7]

        ans_list = [ot_ans_1]
        if ot_ans_2 != None:
            ans_list.append(ot_ans_2)
        if ot_ans_3 != None:
            ans_list.append(ot_ans_3)
        if ot_ans_4 != None:
            ans_list.append(ot_ans_4)

        random.shuffle(ans_list)
        correct_ans_index = random.randint(0, len(ans_list)-1)
        move_ans = ans_list[correct_ans_index]
        ans_list[correct_ans_index] = correct_ans
        ans_list.append(move_ans)

        view = discord.ui.View(timeout=20, disable_on_timeout=True)

        embed = discord.Embed(
            title=f"[#DT{id}] {questdesc}",
            color=0xFFCC00,
        )
        embed.set_image(url=img)
        ans = 1
        for ansloop in ans_list:
            embed.add_field(name=f"OPTION {ans}", value=ansloop, inline=False)

            if ans-1 == correct_ans_index:
                view.add_item(
                    QuizButtons(option=f"OPTION {ans}", correct=True, question_id=id, database="design_trivia")
                )
            else:
                view.add_item(
                    QuizButtons(option=f"OPTION {ans}", correct=False, question_id=id, database="design_trivia")
                )

            ans += 1

        await ctx.respond(embed=embed,view=view)








def setup(client):
    client.add_cog(Quiz(client))