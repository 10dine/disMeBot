import os 
import re
import shutil
import asyncio  
import discord
from dotenv import load_dotenv
from google_images_search import GoogleImagesSearch #publicly available api (unoffical)
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

load_dotenv()  #loads .env
TOKKE = os.getenv('DISCORD_TOKEN')              #gets token from env
GDK = os.getenv('GDev_api_key')                 #get google dev key
GCS = os.getenv('Gcs_link')                     # gets google custome search engine code

client = discord.Client()                       # dont know honestly

@client.event                                   # starts the discord thing i think

async def on_message(message):                  #i think its a loop funtion that waits for command 
    if message.content.startswith('+disMe'):    #checks if message starts with command
        
        guild = str(message.guild)
        guild_Dir = '{}'.format(guild)  #creates string path for directory for guild
        guild_Dir_os = '{}/'.format(guild)

        filelist = [ f for f in os.listdir(guild_Dir)]
        for f in filelist:
            os.remove(os.path.join(guild_Dir_os, f)) #deletes temp files to save space

        
        channel = message.channel          #assigns the message channel a easier variable
        mesid = message.id              
        mesidstr =str(mesid)

        await channel.send('Ok!')               #sends a confirmation
        msg = message.content                   #takes the whole string of the message
        msg_list =re.split(':',msg)             #splits the string into parts

        s_params = {                            #parameters to use for google image search
            'q' : msg_list[1],                  
            'num' : 1,
            'fileType': 'jpg|png'
        }

        gis = GoogleImagesSearch(GDK, GCS)      #sets up google search image class

        gis.search(search_params=s_params, path_to_dir=guild_Dir, custom_image_name=mesidstr) #cant set download to source folder
        
        pic_ext = ''

        piclist = [ p for p in os.listdir(guild_Dir) ]
        for p in piclist:
            if p.endswith('png'):
                pic_ext = 'png'
            else:
                pic_ext = 'jpg'

        picdir = '{}/{}.{}'.format(guild_Dir, mesidstr, pic_ext)   #makes variable for the path
        picdirsave = '{}/{}.png'.format(guild_Dir, mesidstr, pic_ext)

        img = Image.open(picdir) #PIL stuff
        width, height = img.size
        if p.endswith('jpg'):
            img = img.convert("RGBA")
        img1 = ImageDraw.Draw(img) 

        myFont = ImageFont.truetype('impact.ttf', 28)

        img1.text((width/2,10), msg_list[2], font=myFont, fill = (255,255,255), anchor='mt', stroke_width=2, stroke_fill=(0,0,0))
        img1.text((width/2,height-10), msg_list[3], font=myFont, fill = (255,255,255), anchor='ms', stroke_width=2, stroke_fill=(0,0,0))

        img.save(picdirsave)

        await channel.send(file=discord.File(picdirsave)) #sends file
        await channel.send("does this work?")

client.run(TOKKE)