import json
import urllib

def getHelp():
  pesan = ""
  pesan += "Megumin Bot is bot to do some stuff\n\n"
  pesan += "**Prefix**\n$\n"
  pesan += "\n**Commands**\n"
  pesan += "Leave Channel - $l\n"
  pesan += "\n**Music**\n"
  pesan += "Play music - $p\n"
  pesan += "Stop music- $s\n"
  pesan += "Skip current song- $n\n"
  pesan += "Check queue- $q\n"
  pesan += "Clear queue- $cl\n"
  pesan += "Check current playing song - $np\n"
  pesan += "Remove song from queue- $r\n"
  pesan += "\n**Special Sound**\n"
  pesan += "$play blok\n"
  pesan += "$play badumtss\n"
  pesan += "$play bangsat\n"
  pesan += "**Translate** (not perfectly working)\n"
  pesan += "Japan-to-Indonesia - $ja_id\n"
  pesan += "Indonesia-to-Japan - $id_ja\n\n"
  pesan += "**Special**\n"
  pesan += "Wangy Template - $wangy\n\n"
  pesan += "\nThe Weeb Behind This Bot:\n"
  pesan += "[Aldy-san](https://github.com/aldy-san) and [Catyousha](https://github.com/Catyousha).\n\n"
  pesan += "See [Github Repo](https://github.com/aldy-san/megumin-bot)."
  return pesan
  
def struct_to_second(dur):
  total = 0
  total += dur.tm_sec
  total += dur.tm_min*60
  total += dur.tm_hour*3600
  return total
def wrapText(pesan):
  temp ="```"
  temp += pesan
  temp += "```"
  return temp
def getTitle(song_url):
  title = ""
  params = {"format": "json", "url": song_url}
  url = "https://www.youtube.com/oembed"
  query_string = urllib.parse.urlencode(params)
  url = url + "?" + query_string
  with urllib.request.urlopen(url) as response:
      response_text = response.read()
      data = json.loads(response_text.decode())
      title += f"[{data['title']}]({song_url})\n"
  return title
