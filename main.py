import discord
import os
import requests
import json
import random
import pandas as pd
import numpy as np
from keep_alive import keep_alive
client = discord.Client()

katain = ["GOBLOK!","TOLOL!", "BAKA!", "BUTA YAROU!"]

dosen = [
  "Kartika",
  "Agusta",
  "Yahahawahyu",
  "tes"
]

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  output = ""
  if message.author == client.user:
    return
  msg = message.content
  if message.content.startswith('$hello'):
    await message.channel.send('Hello!')

  if message.content.startswith('$megumin'):
    await message.channel.send('Wangy Wangy')

  if message.content.startswith('$quote'):
    quote = get_quote()
    await message.channel.send(quote)

  if any(word in msg for word in dosen):
    await message.channel.send(random.choice(katain))

  if msg.startswith('$regLinier'):
    input_msg = msg.split("$regLinier ",1)[1].split(";")
    if(input_msg[0] == "help"):
      output += "Contoh Input = $regLinier 1 2 3 4 5;1.0 2.0 3.0 4.0 5.0"
    else:
      input_x = [ float(x) for x in input_msg[0].split(" ")]
      input_y = [ float(x) for x in input_msg[1].split(" ")]
      if(len(input_x) != len(input_y)):
        output += "Inputnya salah Blokk!!"
      else: 
        input_x = np.array([input_x])
        input_y = np.array([input_y])
        base_tabel = {'xᵢ': [x for x in input_x[0]],
            'yᵢ': [y for y in input_y[0]],
            'xᵢ²': [pow(x,2) for x in input_x[0]],
            'xᵢyᵢ': [x * y for x,y in zip(input_x[0], input_y[0])]}

        tabel = pd.DataFrame(base_tabel)
        base_sum_tabel = dict()
        for x in tabel:
            base_sum_tabel[f'Σ{x}'] = tabel[x].sum()

        sum_tabel = pd.DataFrame(base_sum_tabel, index=[0])
        output += tabel.to_string(index=False)
        output += "\n"
        output += sum_tabel.to_string(index=False)
        output += "\n\nDidapat SPL:\n"
        output += f"{len(input_x[0])}a₀ + {sum_tabel['Σxᵢ'][0]}a₁ = {sum_tabel['Σyᵢ'][0]}"

        spl_konst = np.array([
                        [len(input_x[0]), sum_tabel['Σxᵢ'][0]],
                        [sum_tabel['Σxᵢ'][0], sum_tabel['Σxᵢ²'][0]]
                        ])
        spl_hasil = np.array([
                              [sum_tabel['Σyᵢ'][0]],
                              [sum_tabel['Σxᵢyᵢ'][0]]
                            ])

        spl_ans = np.linalg.solve(spl_konst, spl_hasil)
        output += "Solusi SPL ini adalah:\n"
        output += f"a₀ = {spl_ans[0][0]}"
        output += f"a₁ = {spl_ans[1][0]}"

        output += "\nRegresi liniarnya adalah:\n"
        output += f"y = {spl_ans[0][0]} + {spl_ans[1][0]}x"

    await message.channel.send(output)   
keep_alive()
client.run(os.getenv('TOKEN'))
