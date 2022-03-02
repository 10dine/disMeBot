import os 
import re
import shutil   #to move files
import asyncio  
import discord
from dotenv import load_dotenv
from google_images_search import GoogleImagesSearch #publicly available api (unoffical)
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

load_dotenv()  #loads .env
TOKKE = os.getenv('DISCORD_TOKEN')              #gets token from env
GDK = os.getenv('GDev_api_key')                 #get dev key
GCS = os.getenv('Gcs_link')                     # gets custome search engine code

client = discord.Client()                       # dont know honestly

@client.event                                   # starts the discord thing i think

async def on_message(message):                  #i think its a loop funtion that waits for command 
    if message.content.startswith('+disMe'):    #checks if message starts with command

        channel = message.channel               #assigns the message channel a easier variable
        await channel.send('Ok!') #sends a confirmation
        msg = message.content                   #takes the whole string of the message
        msg_list =re.split(':',msg)             #splits the string into parts

        s_params = {                            #parameters to use for google image search
            'q' : msg_list[1],                  
            'num' : 1,
            'fileType': 'png'
        }

        gis = GoogleImagesSearch(GDK, GCS)      #sets up google search image class

        gis.search(search_params=s_params, path_to_dir='temp', custom_image_name='temp', width=256, height=256) 

        img = Image.open('temp/temp.png')
        img1 = ImageDraw.Draw(img)
        myFont = ImageFont.truetype('impact.ttf', 28)

        img1.text((128,10), msg_list[2], font=myFont, fill = (255,255,255), anchor='mt', stroke_width=2, stroke_fill=(0,0,0))
        img1.text((128,246), msg_list[3], font=myFont, fill = (255,255,255), anchor='ms', stroke_width=2, stroke_fill=(0,0,0))
        img.save("temp/temp2.png")

        shutil.move('temp/temp.png', 'temp.png')
        shutil.move('temp/temp2.png', 'temp2.png')

        fille = discord.File('temp2.png')

        await channel.send(file=discord.File('temp2.png'))
        await channel.send("does this work?")

        await asyncio.sleep(10)
client.run(TOKKE)