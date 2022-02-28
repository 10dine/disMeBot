import os
import discord
from dotenv import load_dotenv
from google_images_search import GoogleImagesSearch
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from googoo import GID

load_dotenv()
TOKKE = os.getenv('BT_token')

GDK = os.getenv('GDev_api_key')
GCS = os.getenv('GCS_Key')

client = discord.Client()

@client.event
try:
    async def on_ready():
        print(f'{client.user} has connected to Discord')
except:
    print('Some Error Occurred!')
try:
    async def on_message(message):
        if message.content.startswith('+disMe'):

            channel = message.channel
            channel.send('Command Recieved!')

            msg = message
            msg_list =msg.replace(':').split()

            mGid = GID(GDK, GCS, msg_list[1])
            mGid.Idown()

            img = Image.open('temp.jpg')
            img1 = ImageDraw.Draw(img)
            myFont = ImageFont.truetype('impact.ttf', 65)

            img1.text((10,10), msg_list[2], font=myFont, fill = (248,248,255))
            img1.text((20,246), msg_list[3], font=myFont, fill = (248,248,255))
            img.save("temp2.jpg")

            channel.send(img)
            channel.send("does this work?")

            os.remove("temp.jpg","temp2.jpg")
        else:
            pass
except:
    print("Something Happened Bro!")





