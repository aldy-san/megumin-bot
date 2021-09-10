import discord
import os
import re
import pafy
import urllib.request
import validators
import time
import math
import json
from datetime import datetime
from googletrans import Translator
from wangy import singkat,panjang
from supp_func import getHelp,getTitle,struct_to_second,wrapText
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
client.remove_command('help')

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  await client.change_presence(activity=discord.Game(name="$help | Megumin "+version))
def is_connected(ctx):
  voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
  return voice_client and voice_client.is_connected()
@client.command(name='help', aliases=['h'])
async def help(ctx):
  pesan = getHelp()
  embed = discord.Embed()
  embed.title = "💥 Welcome to Megumin "+version+" 💥"
  embed.description = pesan
  embed.color = discord.Colour.red()
  await ctx.send(embed=embed)


#MUSIC
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}
start = None
song_queue=[]
duration_queue=[]
queue_now = int(0)

def play_next(ctx):
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  global start
  global queue_now
  if (queue_now < len(song_queue)):    
      song = pafy.new(song_queue[queue_now]) 
      audio = song.getbestaudio()
      start = datetime.now()
      voice.play(discord.FFmpegPCMAudio(audio.url, **FFMPEG_OPTIONS), after=lambda x=None: play_next(ctx))
      voice.is_playing()
      queue_now += int(1)
      print("queue: "+str(queue_now))
  else:
    queue_now = 0
    voice.stop()
    
@client.command(name='nowPlaying', aliases=['np'])
async def nowPlaying(ctx):
  embed = discord.Embed()
  embed.color = discord.Colour.red() 
  if len(song_queue) >= 1:
    embed.title = "Now Playing"
    pesan = getTitle(song_queue[queue_now]) + "\n"
    global start
    current = datetime.now() - start
    dur = time.strptime(duration_queue[queue_now], '%H:%M:%S')
    percent = math.floor((current.seconds/struct_to_second(dur))*20)
    for x in range(20):
      if x == percent:
        pesan += "㊗️"
      else:
        pesan += "▬"
    pesan += " " + str(current)[:7]+"/"+duration_queue[queue_now]
    embed.description = pesan
  else:
    embed.title = "No Song is Played"
  await ctx.send(embed=embed)

@client.command(name='next', aliases=['n'])
async def next(ctx):
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  voice.stop()
  print(song_queue)
  embed = discord.Embed()
  embed.title = "Playing"
  embed.description = getTitle(song_queue[queue_now])
  embed.color = discord.Colour.red() 
  await ctx.send(embed=embed)

@client.command(name='play', aliases=['p'])
async def play(ctx, *arg):
  voiceChannel = ctx.author.voice.channel
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if voiceChannel == None:
    await ctx.send("Masuk channel dulu la Goblok")
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
  elif arg[0] == "gurenge":
    voice.play(discord.FFmpegPCMAudio("audio/gurenge.mp3"))
  else:
    embed = discord.Embed()
    embed.color = discord.Colour.red() 
    arg = '+'.join(arg)
    if validators.url(arg):
      embed.description = getTitle(arg)
      song_queue.append(arg)
      embed.title = "Added to queue"
      if not voice.is_playing():
        song = pafy.new(arg)  
        audio = song.getbestaudio() 
        duration_queue.append(song.duration)
        voice.play(discord.FFmpegPCMAudio(audio.url, **FFMPEG_OPTIONS), after=lambda x=None: play_next(ctx))
        voice.is_playing()
      await ctx.send(embed=embed)
    else:
      search = arg
      html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search)
      video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
      song_url = "https://www.youtube.com/watch?v=" + video_ids[0]
      embed.description = getTitle(song_url)
      song_queue.append(song_url)
      embed.title = "Added to queue"
      global start
      start = datetime.now()
      song = pafy.new(song_url)
      duration_queue.append(song.duration)
      if not voice.is_playing():
        audio = song.getbestaudio()
        voice.play(discord.FFmpegPCMAudio(audio.url, **FFMPEG_OPTIONS), after=lambda x=None: play_next(ctx))
        voice.is_playing()
      await ctx.send(embed=embed)

@client.command(name='queue', aliases=['q'])
async def queue(ctx):
  queue = ""
  embed = discord.Embed()
  embed.color = discord.Colour.red() 
  if len(song_queue)==0:
    embed.title = "The Queue is Empty"
  else:
    embed.title = "QUEUE"
  for idx, x in enumerate(song_queue):
    params = {"format": "json", "url": x}
    url = "https://www.youtube.com/oembed"
    query_string = urllib.parse.urlencode(params)
    url = url + "?" + query_string
    with urllib.request.urlopen(url) as response:
        response_text = response.read()
        data = json.loads(response_text.decode())
        print(idx)
        print("now: "+str(queue_now))
        if (idx == queue_now):
          queue += "=>"  
        queue += f"[{idx+1}. {(data['title'][:43] + '..') if len(data['title']) > 40 else data['title']}]({x}) "+duration_queue[idx]+"left\n"
  embed.description = queue
  await ctx.send(embed=embed)   

@client.command(name='stop', aliases=['s'])
async def stop(ctx):
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  voice.stop()

@client.command(name='remove', aliases=['r'])
async def remove(ctx, arg):
  song_idx = int(arg) - 1
  if(song_idx == 0):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()
  else:
    duration_queue.pop(song_idx)
    song_queue.pop(song_idx)
    await ctx.send("Successfully remove song")

@client.command(name='leave', aliases=['l'])
async def leave(ctx):
  voice = ctx.voice_client
  if voice is None:
      return await ctx.send("Bot is not in a voice channel")
  else:
    await voice.disconnect()

@client.command(name='clear', aliases=['cl'])
async def clear(ctx):
  del song_queue[:]
  del duration_queue[:]
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  voice.stop()
  await ctx.send("Successfully clear queue")
  
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
@client.command()
async def wc(ctx):
  await ctx.send(file=discord.File('asset/wc.jpg'))
@client.command()
async def weak(ctx):
  await ctx.send(file=discord.File('asset/weak.jpg'))

@client.event
async def on_message(message):
  await client.process_commands(message)
  if message.author == client.user:
    return
    
keep_alive()
try:
    client.run(os.getenv('TOKEN'))
except Exception as e:
    print(e.response)