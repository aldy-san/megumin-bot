import discord
import os
import random
import re
import pafy
import urllib.request
import validators
import json
import urllib

from googletrans import Translator
from functions import *
from hummingCode import *
from interpolasi import *
from wangy import *
from discord.ext import commands
from keep_alive import keep_alive

client = discord.Client()
version = "0.4.0v"
errorMsg = "Ada error apa mbuh ga tau, ga ngurus.\nCek lagi input nya gan"
errorEmbed = discord.Embed()
errorEmbed.title = "!!! ERROR !!!"
errorEmbed.description = errorMsg
errorEmbed.color = discord.Colour.red()
client = commands.Bot(command_prefix="$")
#Music
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}
client.remove_command('help')
@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  await client.change_presence(activity=discord.Game(name="$help | Megumin "+version))
def is_connected(ctx):
  voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
  return voice_client and voice_client.is_connected()
@client.command()
async def help(ctx):
  pesan = ""
  pesan += "Megumin Bot is bot to do some stuff\n\n"
  pesan += "**Prefix**\n$\n"
  pesan += "\n**Commands**\n"
  pesan += "Leave Channel - $leave\n"
  pesan += "\n**Music**\n"
  pesan += "Play music - $play\n"
  pesan += "Stop music- $stop\n"
  pesan += "Skip current song- $next\n"
  pesan += "Check queue- $queue\n"
  pesan += "Remove song from queue- $remove\n"
  pesan += "\n**Special Sound**\n"
  pesan += "$play blok\n"
  pesan += "$play badumtss\n"
  pesan += "$play bangsat\n"
  pesan += "\n**Calculate**\n"
  pesan += "Regresi Linier - $regLinier\n"
  pesan += "Regresi Kuadratik - $regKuadratik\n"
  pesan += "Gauss Jordan - $gaussJordan\n"
  pesan += "Interpol Linier - $interpolLinier\n"
  pesan += "Humming Code - $hummingCode\n\n"
  pesan += "**Translate** (not perfectly working)\n"
  pesan += "Japan-to-Indonesia - $ja_id\n"
  pesan += "Indonesia-to-Japan - $id_ja\n\n"
  pesan += "**Special**\n"
  pesan += "Wangy Template - $wangy\n\n"
  pesan += "Type help after prefix to see Example input\n"
  pesan += "Ex: $regLinier help\n"
  pesan += "\nThe Weeb Behind This Bot:\n"
  pesan += "[Aldy-san](https://github.com/aldy-san) and [Catyousha](https://github.com/Catyousha).\n\n"
  pesan += "See [Github Repo](https://github.com/aldy-san/megumin-bot)."
  embed = discord.Embed()
  embed.title = "💥 Welcome to Megumin "+version+" 💥"
  embed.description = pesan
  embed.color = discord.Colour.red()
  await ctx.send(embed=embed)
#SPECIAL
@client.command()
async def hello(ctx):
  await ctx.send(wrapText("Hello! 🥱"))
@client.command()
async def wangy(ctx, *arg):
  msg = ' '.join(arg)
  if "help" in msg:
    pesan = "Contoh Input:\n"
    pesan += "$wangy Megumin"
    await ctx.send(wrapText(pesan))
  else:
    input_msg = msg
    embed = discord.Embed()
    param = input_msg.split(" ")
    if len(param) > 1:
      embed.title = "❤️ ❤️ ❤️ Wangy Wangy "+param[0]+" Wangy ❤️ ❤️ ❤️"
      embed.description = panjang(input_msg)
    else:
      embed.title = "❤️ ❤️ ❤️ Wangy Wangy "+input_msg+" Wangy ❤️ ❤️ ❤️"
      embed.description = singkat(input_msg)
    embed.color = discord.Colour.red() 
    await ctx.send(embed=embed)

#MUSIC
song_queue = []
def play_next(ctx):
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if len(song_queue) > 1:
      del song_queue[0]
      song = pafy.new(song_queue[0]) 
      audio = song.getbestaudio()
      voice.stop()
      voice.play(discord.FFmpegPCMAudio(audio.url, **FFMPEG_OPTIONS), after=lambda x=None: play_next(ctx))
      voice.is_playing()
  else:
    del song_queue[0]
    voice.stop()
@client.command()
async def next(ctx):
  play_next(ctx)
@client.command()
async def play(ctx, *arg):
  voiceChannel = ctx.author.voice.channel
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if voice == None:
    await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  else:
    await voice.move_to(voiceChannel)
  if arg[0] == "blok":
    voice.play(discord.FFmpegPCMAudio("audio/blok.mp3"))
  elif arg[0] == "badumtss":
    voice.play(discord.FFmpegPCMAudio("audio/badumtss.mp3"))
  elif arg[0] == "bangsat":
    voice.play(discord.FFmpegPCMAudio("audio/bangsat.mp3"))
  else:
    arg = '+'.join(arg)
    if validators.url(arg):
      song_queue.append(arg)
      if not voice.is_playing():
        song = pafy.new(arg)  
        audio = song.getbestaudio() 
        voice.play(discord.FFmpegPCMAudio(audio.url, **FFMPEG_OPTIONS), after=lambda x=None: play_next(ctx))
        voice.is_playing()
      else:
          await ctx.send("Added to queue")
    else:
      search = arg
      html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search)
      video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
      song_url = "https://www.youtube.com/watch?v=" + video_ids[0]
      
      await ctx.send(song_url)
      song_queue.append(song_url)
      if not voice.is_playing():
        song = pafy.new(song_url) 
        audio = song.getbestaudio()
        voice.play(discord.FFmpegPCMAudio(audio.url, **FFMPEG_OPTIONS), after=lambda x=None: play_next(ctx))
        voice.is_playing()
      else:
          await ctx.send("Added to queue")
@client.command()
async def queue(ctx):
  queue = ""
  embed = discord.Embed()
  embed.title = "QUEUE"
  for idx, x in enumerate(song_queue):
    params = {"format": "json", "url": x}
    url = "https://www.youtube.com/oembed"
    query_string = urllib.parse.urlencode(params)
    url = url + "?" + query_string
    with urllib.request.urlopen(url) as response:
        response_text = response.read()
        data = json.loads(response_text.decode())
        queue += f"[{idx+1}. {data['title']}]({x})\n"
  embed.description = queue
  await ctx.send(embed=embed)    
@client.command()
async def stop(ctx):
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  voice.stop()
@client.command()
async def remove(ctx, arg):
  song_idx = int(arg) - 1
  if(song_idx == 0):
    play_next(ctx)
  else:
    song_queue.pop(song_idx)
    await ctx.send("Successfully remove song")
@client.command()
async def leave(ctx):
  voice = ctx.voice_client
  if voice is None:
      return await ctx.send("Bot is not in a voice channel")
  else:
    await voice.disconnect()

#TRANSLATE
@client.command()
async def ja_id(ctx, *arg):
  msg = ' '.join(arg)
  if "help" in msg:
    pesan = "Contoh Input:\n"
    pesan += "$ja_id murasaki"
    await ctx.send(wrapText(pesan))
  else:
    translator = Translator()  
    translate_text = translator.translate(msg,src="ja", dest='id')
    translate_text = translate_text.__dict__()["text"]
    await ctx.send(wrapText(translate_text))
@client.command()
async def id_ja(ctx, *arg):
  msg = ' '.join(arg)
  if "help" in msg:
    pesan = "Contoh Input:\n"
    pesan += "$id_ja ungu"
    await ctx.send(wrapText(pesan))
  else:
    translator = Translator()  
    translate_text = translator.translate(msg,src="id", dest='ja')
    translate_text = translate_text.__dict__()["text"]
    await ctx.send(wrapText(translate_text))
#KONUM & KDJK
@client.command()
async def regLinier(ctx, *arg):
  msg = ' '.join(arg)
  input_msg = msg.split(";")
  if(input_msg[0] == "help"):
    pesan = "Contoh Input = $regLinier 1 2 3 4 5;1.0 2.0 3.0 4.0 5.0"
    await ctx.send(wrapText(pesan))
  else:
    try:
      input_x = [ float(x) for x in input_msg[0].split(" ")]
      input_y = [ float(x) for x in input_msg[1].split(" ")]
      pesan, grafik = getRegLinear(input_x, input_y)
      await ctx.send(wrapText(pesan))
      await ctx.send(file=grafik)
    except:
      await ctx.send(embed=errorEmbed)
@client.command()
async def regKuadratik(ctx, *arg):
  msg = ' '.join(arg)
  input_msg = msg.split(";")
  if(input_msg[0] == "help"):
    pesan = "Contoh Input = $regKuadratik 1 2 3 4 5;1.0 2.0 3.0 4.0 5.0"
    await ctx.send(wrapText(pesan))
  else:
    try:
      input_x = [ float(x) for x in input_msg[0].split(" ")]
      input_y = [ float(x) for x in input_msg[1].split(" ")]
      pesan, grafik = getRegKuadratik(input_x, input_y)
      await ctx.send(wrapText(pesan))
      await ctx.send(file=grafik)
    except:
      await ctx.send(embed=errorEmbed)
@client.command()
async def gaussJordan(ctx, *arg):
  msg = ' '.join(arg)
  await ctx.send(msg)
  if "help" in msg:
    pesan = "Contoh Input:\n"
    pesan += "$gaussJordan\n1, 9, 0;\n3, 5, 6;\n6, 0, 4;\nand\n6, 0, 4"
    await ctx.send(wrapText(pesan))
  else:
    try:
      input_msg = msg
      spl_konst = input_msg.split("and ")[0].split("; ")
      spl_hasil = input_msg.split("and ")[1].split(", ")
      n = len(spl_konst) - 1
      temp =[]
      spl_konst.pop()
      for x in spl_konst:
          temp += [float(y) for y in x.split(", ")]
      spl_konst = np.reshape( np.array(temp), (-1, n))
      spl_hasil = np.array([[float(x) for x in spl_hasil]])
      pesan = stepGaussJordan(spl_konst,spl_hasil)
      await ctx.send(wrapText(pesan))
    except:
      await ctx.send(embed=errorEmbed)
@client.command()
async def interpolLinier(ctx, *arg):
  msg = ' '.join(arg)
  if "help" in msg:
    pesan = "Contoh Input:\n"
    pesan += "$interpolLinier y=2 titik_1=1,5 titik_2=4,2"
    await ctx.send(wrapText(pesan))
  else:
    try:
      await ctx.send(wrapText(linier(msg)))
    except:
      await ctx.send(embed=errorEmbed)
@client.command()
async def hummingCode(ctx, *arg):
  msg = ' '.join(arg)
  input_msg = msg
  if(input_msg[1] == 'help'):
    pesan = "Contoh Input = $hummingCode 01010011 00110001 00100000 01010100 01001001"
    await ctx.send(wrapText(pesan))
  else:
    try:
      pesan = humming_code(input_msg[1])
      await ctx.send(wrapText(pesan))
    except:
      await ctx.send(embed=errorEmbed)

@client.event
async def on_message(message):
  await client.process_commands(message)
  if message.author == client.user:
    return
    
keep_alive()
client.run(os.getenv('TOKEN'))