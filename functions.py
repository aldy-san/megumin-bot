import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import discord

def wrapText(pesan):
  temp ="```"
  temp += pesan
  temp += "```"
  return temp
def getRegKuadratik(input_x, input_y):
  output = ""
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