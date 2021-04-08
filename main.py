import discord
import os
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
    pesan += "Megumin Bot is bot to Calculate some stuff\n\n"
    pesan += "**Prefix**\n$\n"
    pesan += "\n**Features**\n"
    pesan += "Regresi Linier - $regLinier\n"
    pesan += "Regresi Kuadratik - $regKuadratik\n"
    pesan += "Gauss Jordan (Only 3x3 Matriks) - $gaussJordan\n\n"
    pesan += "Type help after prefix to see Example input\n"
    pesan += "Ex: $regLinier help\n"
    pesan += "\nThe Weeb Behind This Bot:\n"
    pesan += "[Aldy-san](https://github.com/aldy-san) and [Catyousha](https://github.com/Catyousha)."
    embed = discord.Embed()
    embed.title = "💥 Welcome to Megumin 0.3v 💥"
    embed.description = pesan
    embed.color = discord.Colour.red()
    await message.channel.send(embed=embed)

  if msg.startswith('$gaussJordan'):
    if "help" in msg:
      pesan = "Contoh Input:\n"
      pesan += "$gaussJordan\n1, 9, 0;\n3, 5, 6;\n6, 0, 4;\nand\n6, 0, 4"
      await message.channel.send(wrapText(pesan))
    else:
      try:
        input_msg = msg.split("$gaussJordan\n")[1]
        spl_konst = input_msg.split("and\n")[0].split(";\n")
        spl_hasil = input_msg.split("and\n")[1].split(",\n")
        spl_konst = np.array([
                    [float(x) for x in spl_konst[0].split(", ")],
                    [float(x) for x in spl_konst[1].split(", ")],
                    [float(x) for x in spl_konst[2].split(", ")],
                    ])
        spl_hasil = np.array([[float(x) for x in spl_hasil[0].split(", ")]])
        pesan = stepGaussJordan(spl_konst,spl_hasil)
        await message.channel.send(wrapText(pesan))
      except:
        await message.channel.send(wrapText("!!! ERROR !!!\nAda error apa mbuh ga tau, ga ngurus."))
      

  if msg.startswith('$regLinier'):
    input_msg = msg.split("$regLinier ",1)[1].split(";")
    if(input_msg[0] == "help"):
      pesan = "Contoh Input = $regLinier 1 2 3 4 5;1.0 2.0 3.0 4.0 5.0"
      await message.channel.send(wrapText(pesan))
    else:
      try:
        input_x = [ float(x) for x in input_msg[0].split(" ")]
        input_y = [ float(x) for x in input_msg[1].split(" ")]
        pesan, grafik = getRegLinear(input_x, input_y)
        await message.channel.send(wrapText(pesan))
        await message.channel.send(file=grafik)
      except:
        await message.channel.send(wrapText("!!! ERROR !!!\nAda error apa mbuh ga tau, ga ngurus."))
    
  if msg.startswith('$regKuadratik'):
    input_msg = msg.split("$regKuadratik ",1)[1].split(";")
    if(input_msg[0] == "help"):
      pesan = "Contoh Input = $regKuadratik 1 2 3 4 5;1.0 2.0 3.0 4.0 5.0"
      await message.channel.send(wrapText(pesan))
    else:
      try:
        input_x = [ float(x) for x in input_msg[0].split(" ")]
        input_y = [ float(x) for x in input_msg[1].split(" ")]
        pesan, grafik = getRegKuadratik(input_x, input_y)
        await message.channel.send(wrapText(pesan))
        await message.channel.send(file=grafik)
      except:
        await message.channel.send(wrapText("!!! ERROR !!!\nAda error apa mbuh ga tau, ga ngurus."))
      
keep_alive()
client.run(os.getenv('TOKEN'))