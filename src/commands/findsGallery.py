import logging
import time
import datetime
from os import path
import os

import discord
from discord import bot
from discord.ext import commands, tasks
from dotenv import load_dotenv



class FindsGallery(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(
            f"Cog {path.basename(__file__).removesuffix('.py')} loaded successfully"
        )

    @commands.Cog.listener()
    async def on_message(self, message):  # FindOfTheWeek
        if message.author.bot:  # is message from bot?
            return

        channel_id_1 = os.getenv("FOTW_CHANNEL_ID_1")
        channel_id_2 = os.getenv("FOTW_CHANNEL_ID_2")
        finds_gallery = os.getenv("FINDS_GALLERY_ID")
        if (str(message.channel.id) != channel_id_1) and (
                str(message.channel.id) != channel_id_2):  # is message sent in right channel?
            # await self.client.process_commands(message)
            return

        if len(message.attachments) == 0:
            return
        else:
            filelist = []
            for file in message.attachments:
                if file.filename.endswith("jpg") \
                        or file.filename.endswith("png") \
                        or file.filename.endswith("JPG") \
                        or file.filename.endswith("PNG"):  # Checks if message has attachments .png or .jpg
                    file = await file.to_file()
                    filelist.append(file)
            channel = self.client.get_channel(
                int(finds_gallery)
            )
            if message.author.nick is None:
                title = message.author.name
            else:
                title = message.author.nick
            embed = discord.Embed(
                title=f"Find by {title}",
                description=message.content,
                color=0xFFCC00,
            )
            embed.add_field(name="Link:", value=message.jump_url, inline=True)

            await channel.send(embed=embed,files=filelist)









def setup(client):
    client.add_cog(FindsGallery(client))