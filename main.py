import discord
import os
import requests
import json
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from keep_alive import keep_alive
client = discord.Client()

katain = ["GOBLOK!","TOLOL!", "BAKA!", "BUTA YAROU!"]

dosen = [
  "Kartika",
  "Agusta",
  "Yahahawahyu",
  "tes"
]
def getRegKuadratik(input_x, input_y):
  output = "```"
  if(len(input_x) != len(input_y)):
    output += "Inputnya salah Blokk!!"
  else:
    input_x = np.array([input_x])
    input_y = np.array([input_y]) 
    base_tabel = {'xᵢ': [x for x in input_x[0]],
         'yᵢ': [y for y in input_y[0]],
         'xᵢ²': [pow(x,2) for x in input_x[0]],
         'xᵢ³': [pow(x,3) for x in input_x[0]],
         'xᵢ⁴': [pow(x,4) for x in input_x[0]],
         'xᵢyᵢ': [x * y for x,y in zip(input_x[0], input_y[0])],
         'xᵢ²yᵢ': [pow(x,2) * y for x,y in zip(input_x[0], input_y[0])]}

    tabel = pd.DataFrame(base_tabel)
    base_sum_tabel = dict()
    for x in tabel:
        base_sum_tabel[f'Σ{x}'] = tabel[x].sum()

    sum_tabel = pd.DataFrame(base_sum_tabel, index=[0])

    output += tabel.to_string(index=False)
    output += "\n"
    output += sum_tabel.to_string(index=False)

    spl_konst = np.array([
                    [len(input_x[0]), sum_tabel['Σxᵢ'][0], sum_tabel['Σxᵢ²'][0]],
                    [sum_tabel['Σxᵢ'][0], sum_tabel['Σxᵢ²'][0], sum_tabel['Σxᵢ³'][0]],
                    [sum_tabel['Σxᵢ²'][0], sum_tabel['Σxᵢ³'][0], sum_tabel['Σxᵢ⁴'][0]]
                    ])
    spl_hasil = np.array([
                          [sum_tabel['Σyᵢ'][0]],
                          [sum_tabel['Σxᵢyᵢ'][0]],
                          [sum_tabel['Σxᵢ²yᵢ'][0]]
                        ])

    output += "\n\nDidapat SPL:\n"
    output += f"{spl_konst[0][0]}a₀ + {spl_konst[0][1]}a₁ + {spl_konst[0][2]}a₂ = {spl_hasil[0][0]}\n"
    output += f"{spl_konst[1][0]}a₀ + {spl_konst[1][1]}a₁ + {spl_konst[1][2]}a₂ = {spl_hasil[1][0]}\n"
    output += f"{spl_konst[2][0]}a₀ + {spl_konst[2][1]}a₁ + {spl_konst[2][2]}a₂ = {spl_hasil[2][0]}\n"
    spl_ans = np.linalg.solve(spl_konst, spl_hasil)
    output += "\nSolusi SPL ini adalah:\n"
    output += f"a₀ = {round(spl_ans[0][0], 5)}\n"
    output += f"a₁ = {round(spl_ans[1][0], 5)}\n"
    output += f"a₂ = {round(spl_ans[2][0], 5)}\n"
    output += "\nRegresi kuadratiknya adalah:\n"
    output += f"y = {round(spl_ans[0][0], 5)} + {round(spl_ans[1][0], 5)}x + {round(spl_ans[2][0], 5)}x²"

    plt.scatter(tabel['xᵢ'], tabel['yᵢ'])
    plt.plot(tabel['xᵢ'], spl_ans[0][0] + spl_ans[1][0] * tabel['xᵢ'] + spl_ans[2][0] * pow(tabel['xᵢ'],2),
            label=f"y = {round(spl_ans[0][0], 5)} + {round(spl_ans[1][0], 5)}x + {round(spl_ans[2][0], 5)}x²",
            c="r")
    plt.xlabel('xᵢ')
    plt.ylabel('yᵢ')
    plt.legend(loc='best', borderaxespad=0.)
    plt.title('Regresi Kuadratik')
    plt.savefig('grafik_kuadratik.png')
    grafik = discord.File('grafik_kuadratik.png')
    plt.close()
  return output, grafik

def getRegLinear(input_x, input_y):
  output = "```"
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
    output += f"{len(input_x[0])}a₀ + {sum_tabel['Σxᵢ'][0]}a₁ {sum_tabel['Σyᵢ'][0]}\n"

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
    output += f"a₀ = {spl_ans[0][0]}\n"
    output += f"a₁ = {spl_ans[1][0]}\n"

    output += "\nRegresi liniernya adalah:\n"
    output += f"y = {spl_ans[0][0]} + {spl_ans[1][0]}x"
    plt.scatter(tabel['xᵢ'], tabel['yᵢ'])
    plt.plot(tabel['xᵢ'], spl_ans[0][0] + spl_ans[1][0] * tabel['xᵢ'],
            label=f"y = {spl_ans[0][0]} + {spl_ans[1][0]}x",
            c="r")
    plt.xlabel('xᵢ')
    plt.ylabel('yᵢ')
    plt.legend(loc='best', borderaxespad=0.)
    plt.title('Regresi Linier')
    plt.savefig('grafik_linier.png')
    grafik = discord.File('grafik_linier.png')
    plt.close()
  return output, grafik

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
  if message.author == client.user:
    return
  msg = message.content
  if msg.startswith('$hello'):
    await message.channel.send('```Hello!```')

  if msg.startswith('$megumin'):
    await message.channel.send('Wangy Wangy')

  if any(word in msg for word in dosen):
    await message.channel.send(random.choice(katain))
  
  if msg == '$megumin help':
    pesan = "```command is just\n"
    pesan += "$regLinier\n"
    pesan += "$regKuadratik\n"
    pesan += "```"
    await message.channel.send(pesan)
  
  if msg.startswith('$regLinier'):
    input_msg = msg.split("$regLinier ",1)[1].split(";")
    if(input_msg[0] == "help"):
      pesan = "```Contoh Input = $regLinier 1 2 3 4 5;1.0 2.0 3.0 4.0 5.0```"
    else:
      input_x = [ float(x) for x in input_msg[0].split(" ")]
      input_y = [ float(x) for x in input_msg[1].split(" ")]
      pesan, grafik = getRegLinear(input_x, input_y)
      pesan += "```"
      await message.channel.send(pesan)
      await message.channel.send(file=grafik)

  if msg.startswith('$regKuadratik'):
    input_msg = msg.split("$regKuadratik ",1)[1].split(";")
    if(input_msg[0] == "help"):
      pesan = "```Contoh Input = $regKuadratik 1 2 3 4 5;1.0 2.0 3.0 4.0 5.0```"
    else:
      input_x = [ float(x) for x in input_msg[0].split(" ")]
      input_y = [ float(x) for x in input_msg[1].split(" ")]
      pesan, grafik = getRegKuadratik(input_x, input_y)
      pesan += "```"
    await message.channel.send(pesan)
    await message.channel.send(file=grafik)
keep_alive()
client.run(os.getenv('TOKEN'))
