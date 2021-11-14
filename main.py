import os, discord
import imagehash
from PIL import Image
import requests
import jpype.imports
from jpype import startJVM, shutdownJVM, java, addClassPath, JClass, JInt
startJVM(convertStrings=False)
import numpy
client = discord.Client()
LOST = []
FOUND = []

@client.event
async def on_ready():
  print(f'{client.user} has connected to Discord!')
  
async def embed(loser, img_url, jump_url, finder, similarity):
    embed=discord.Embed(title="Is this your cat?", url=jump_url, description="We have calculated a " + str(round((similarity + 1) * 50,2)) + "% similarity between your cat and this image" , color=0x00ffff)
    embed.set_author(name=finder.name+"#"+finder.discriminator, icon_url=finder.avatar_url)
    embed.set_image(url=img_url)
    await loser.send(embed=embed)

@client.event
async def on_message(message):
    global LOST, FOUND
    for i in message.attachments:
        Data = JClass('Output');
        cat = Data()
        Attributes = [i-127 for i in cat.getAttributes(i.url)]
        file = Image.open(requests.get(i.url, stream=True).raw)
        #Attributes.append(int(str(imagehash.average_hash(file)), 16)/36028797018963967-127)
        #Attributes.append(int(str(imagehash.phash(file)), 16)/36028797018963967-127)
        #Attributes.append(int(str(imagehash.dhash(file)), 16)/36028797018963967-127)
        #Attributes.append(int(str(imagehash.whash(file)), 16)/36028797018963967-127)
        #Attributes.append(int(str(imagehash.colorhash(file)), 16)/36028797018963967-127)
        print(Attributes)
        if "lost" in message.content.lower():
            LOST.append([message, Attributes, i.url])
            for j in FOUND:
                similarity = round(numpy.dot(Attributes,j[1])/(numpy.linalg.norm(Attributes)*numpy.linalg.norm(j[1])),2)
                if similarity > 0.5:
                    await embed(message.author, j[2], j[0].jump_url, j[0].author, similarity)
        elif "found" in message.content.lower():
            FOUND.append([message, Attributes, i.url])
            for j in LOST:
                similarity = round(numpy.dot(Attributes,j[1])/(numpy.linalg.norm(Attributes)*numpy.linalg.norm(j[1])),2)
                if similarity > 0.5:
                    await embed(j[0].author, i.url, message.jump_url, message.author, similarity)

        
client.run(os.environ['BOT_TOKEN'])
