import logging, requests
import imageio
import numpy as np
from PIL import Image
from os import path, getenv

import discord
from discord import bot
from discord.commands import option, SlashCommandGroup
from discord.ext import commands


class EuroBillTracker(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.sessid = False #whether or not the session ID is set or not

    ebt = SlashCommandGroup("ebt", "Get statistics about EuroBillTracker")
    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(
            f"Cog {path.basename(__file__).removesuffix('.py')} loaded successfully"
        )


    def login(self):
        """Login to the EBT app to get sess ID"""
        url = 'https://api.eurobilltracker.com/?m=login&v=2'
        json = {
            'my_email': getenv('EBT_EMAIL'),
            'my_password': getenv('EBT_PASS')
        }

        response = requests.post(url, data=json)
        try:
            self.sessid = response.json()['sessionid']
            return True
        except:
            return False #the session ID request failed, for whatever reason

    @ebt.command(description='test command')
    @option(
        "user",
        description="Get information about a specific user given the username",
        required=True,
    )
    async def user(self, ctx, user):
        await ctx.defer()

        if self.sessid is False:
            self.login()
            if not self.sessid:
                await ctx.respond('The API session ID could not be obtained (please contact a developer).')
                return

        #perform search to get user id
        search_url = f'https://api.eurobilltracker.com/?m=search&v=1&PHPSESSID={self.sessid}&find={user}&what=1'
        search_response = requests.get(search_url)
        search_response.encoding = 'utf-8-sig'
        if search_response.json()['nr_users'] == 0:
            await ctx.respond(f'No such user could be found. Did you type the username properly?')
            return

        user_id = search_response.json()['users'][0]['id']

        #get info about user id
        user_url = f'https://api.eurobilltracker.com/?m=globalstats_profile_user&v=1&PHPSESSID={self.sessid}&user_id={user_id}&language=en'
        user_response = requests.get(user_url)
        user_response.encoding = 'utf-8-sig'

        print(user_response.json())
        #assemble embed
        embed = discord.Embed(
            title=f'EuroBillTracker User: {user_response.json()["data"]["user_name"]}',
            url=f'https://en.eurobilltracker.com/profile/?user={user_id}',
            color=0x5f7797
        )
        embed.add_field(name='Location', value=f'{user_response.json()["data"]["home_location_name"]}, {user_response.json()["data"]["home_country_name"]}')
        embed.add_field(name='Join Date', value=user_response.json()['data']['join_date'])
        embed.add_field(name='Last Active', value=user_response.json()['data']['last_active_timestamp'])
        embed.add_field(name='Total Notes Entered', value=user_response.json()["data"]["total_notes"])
        embed.add_field(name='Total Hits', value=user_response.json()["data"]["total_hits"])
        embed.add_field(name='Hit Ratio', value=f'1 : {float(user_response.json()["data"]["total_notes"])/float(user_response.json()["data"]["total_hits"]):.2f}')

        #create gif
        imgcount = 0
        if user_response.json()["data"]["img_url_notes_europe"] is not None:
            imgcount += 1
            img_data = requests.get(user_response.json()["data"]["img_url_notes_europe"]).content
            with open('data//EBT_Notes_map.jpg', 'wb') as handler:
                handler.write(img_data)
        if user_response.json()["data"]["img_url_hits_europe"] is not None:
            imgcount += 1
            img_data = requests.get(user_response.json()["data"]["img_url_hits_europe"]).content
            with open('data//EBT_Hits_map.jpg', 'wb') as handler:
                handler.write(img_data)
        if imgcount != 0:
            images = ([Image.open('data//EBT_Notes_map.jpg')]*50) + ([Image.open('data//EBT_Hits_map.jpg')]*50)

            images[0].save('data//EBT.gif',
                           save_all=True, append_images=images[1:], optimize=False, duration=100, loop=0)

            file = discord.File('data//EBT.gif', filename='EBT.gif')
            embed.set_image(url='attachment://EBT.gif')
            await ctx.respond(file=file,embed=embed)
            return

        await ctx.respond(embed=embed)



def setup(client):
    client.add_cog(EuroBillTracker(client))
