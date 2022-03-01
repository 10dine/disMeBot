import os
import re
import shutil
import asyncio
import discord
from dotenv import load_dotenv
from google_images_search import GoogleImagesSearch
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

load_dotenv()
TOKKE = os.getenv('DISCORD_TOKEN')
GDK = os.getenv('GDev_api_key')
GCS = os.getenv('Gcs_link')

client = discord.Client()

@client.event

async def on_message(message):
    if message.content.startswith('+disMe'):

        channel = message.channel
        await channel.send('Command Recieved!')
        msg = message.content
        msg_list =re.split(':',msg)

        s_params = {
            'q' : msg_list[1],
            'num' : 1,
            'fileType': 'png'
        }

        gis = GoogleImagesSearch(GDK, GCS)

        gis.search(search_params=s_params, path_to_dir='temp', custom_image_name='temp', width=256, height=256)

        img = Image.open('temp/temp.png')
        img1 = ImageDraw.Draw(img)
        myFont = ImageFont.truetype('impact.ttf', 28)

        img1.text((100,10), msg_list[2], font=myFont, fill = (192,192,192))
        img1.text((80,226), msg_list[3], font=myFont, fill = (192,192,192))
        img.save("temp/temp2.png")

        shutil.move('temp/temp.png', 'temp.png')
        shutil.move('temp/temp2.png', 'temp2.png')

        fille = discord.File('temp2.png')

        await channel.send(file=discord.File('temp2.png'))
        await channel.send("does this work?")

        await asyncio.sleep(10)
client.run(TOKKE)