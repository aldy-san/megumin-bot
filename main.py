import discord
import os
import requests
import json
import random
from functions import *
from keep_alive import keep_alive
client = discord.Client()

katain = ["GOBLOK!","TOLOL!", "BAKA!", "BUTA YAROU!"]
dosen = ["Kartika","Agusta","Yahahawahyu"]
  
@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
@client.event
async def on_message(message):
  if message.author == client.user:
    return
  msg = message.content
  if msg.startswith('$hello'):
    await message.channel.send(wrapText("Hello! 🥱"))


  if any(word in msg for word in dosen):
    await message.channel.send(random.choice(katain))
  
  if msg == '$help':
    pesan = ""
    pesan += "Welcome to Megumin 0.2v 🖐️\n"
    pesan += "Features:\n"
    pesan += "$regLinier\n"
    pesan += "$regKuadratik\n"
    pesan += "\nThe Weeb Behind This Code:"
    embed = discord.Embed()
    embed.description = "[Aldy-san](https://github.com/aldy-san) and [Catyousha](https://github.com/Catyousha)."
    await message.channel.send(wrapText(pesan))
    await message.channel.send(embed=embed)
  
  if msg.startswith('$regLinier'):
    input_msg = msg.split("$regLinier ",1)[1].split(";")
    if(input_msg[0] == "help"):
      pesan = "Contoh Input = $regLinier 1 2 3 4 5;1.0 2.0 3.0 4.0 5.0"
    else:
      input_x = [ float(x) for x in input_msg[0].split(" ")]
      input_y = [ float(x) for x in input_msg[1].split(" ")]
      pesan, grafik = getRegLinear(input_x, input_y)
      await message.channel.send(wrapText(pesan))
      await message.channel.send(file=grafik)

  if msg.startswith('$regKuadratik'):
    input_msg = msg.split("$regKuadratik ",1)[1].split(";")
    if(input_msg[0] == "help"):
      pesan = "Contoh Input = $regKuadratik 1 2 3 4 5;1.0 2.0 3.0 4.0 5.0"
    else:
      input_x = [ float(x) for x in input_msg[0].split(" ")]
      input_y = [ float(x) for x in input_msg[1].split(" ")]
      pesan, grafik = getRegKuadratik(input_x, input_y)
    await message.channel.send(wrapText(pesan))
    await message.channel.send(file=grafik)
keep_alive()
client.run(os.getenv('TOKEN'))
