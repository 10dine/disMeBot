#This bot uses the old bot 


import os 
import re
import shutil
import asyncio  
import discord
from dotenv import load_dotenv
from google_images_search import GoogleImagesSearch         #publicly available api (unoffical)
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

load_dotenv()                                               #loads .env
TOKEN = os.getenv('DISCORD_TOKEN')                          #gets discord token from env
GDK = os.getenv('GDev_api_key')                             #get google dev key (GDK)
GCS = os.getenv('Gcs_link')                                 #gets google custom search engine code 

client = discord.Client()                                   #Sets Discord bot client to a variable

@client.event                                               #Starts the bot.

async def on_message(message):                              #Waits for message on the servers the bot is on.
    if message.content.startswith('+disMe'):                #If message starts with bot command then main function is started.
        
        guild = str(message.guild)                          #creates a string of the servers name
        guild_Dir = '{}'.format(guild)                      #creates string of server
        guild_Dir_os = '{}/'.format(guild)                  #creates string of server with slash for path

        filelist = [f for f in os.listdir(guild_Dir)]       #gets list of files from server folder
        for f in filelist:
            os.remove(os.path.join(guild_Dir_os, f))        #deletes temp files

        
        channel = message.channel                           #assigns the message channel to a variable
        mes_id_str =str(message.id )                          #assigns the message id as a string to a variable

        await channel.send('Ok!')                           #sends a confirmation
        msg = message.content                               #takes the whole string of the message
        msg_list =re.split(':', msg)                        #splits the string into parts (command, search term, Top text, Bottom text)

        s_params = {                                        #parameters to use for google image search
            'q' : msg_list[1],                              #q is the search term
            'num' : 1,                                      #num is the number of images requested
            'fileType': 'jpg|png'                           #filetype 
        }

        gis = GoogleImagesSearch(GDK, GCS)                  #sets up google search image class

        gis.search(search_params=s_params, path_to_dir=guild_Dir, custom_image_name=mes_id_str) #cant set download to source folder
        
        pic_ext = ''                                        #empty variable for saving extension of picture recieved from google images

        piclist = [ p for p in os.listdir(guild_Dir) ]      #creates list of files within server folder
        for p in piclist:                                   #sets picture extension, this is ffor the purpose of PIL save image function
            if p.endswith('png'):
                pic_ext = 'png'
            else:
                pic_ext = 'jpg'

        picdir = '{}/{}.{}'.format(guild_Dir, mes_id_str, pic_ext)      #makes variable for the path
        picdirsave = '{}/{}.png'.format(guild_Dir, mes_id_str, pic_ext) #

        img = Image.open(picdir)                            #PIL open image funciton
        width, height = img.size                            #sets height and width for PIL
        if p.endswith('jpg'):           
            img = img.convert("RGBA")
        img1 = ImageDraw.Draw(img) 

        myFont = ImageFont.truetype('impact.ttf', 28)

        img1.text((width/2,height-10), msg_list[2], font=myFont, fill = (255,255,255), anchor='mt', stroke_width=2, stroke_fill=(0,0,0))
        img1.text((width/2,height-10), msg_list[3], font=myFont, fill = (255,255,255), anchor='ms', stroke_width=2, stroke_fill=(0,0,0))

        img.save(picdirsave)

        await channel.send(file=discord.File(picdirsave)) #sends file
        await channel.send("does this work?")

client.run(TOKEN)