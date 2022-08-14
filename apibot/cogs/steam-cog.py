import json
from datetime import datetime
import urllib
import re
from urllib import response
import requests
from discord.ext import commands
import discord
import flag
class steam(commands.Cog):
    def __init__(self, client):
          self.client = client 
    @commands.command()
    async def stprofile(self, ctx, name):
         x = requests.get(f"http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=964A0610CCE27D7155ED1B9E09C32BFE&vanityurl={name}")
         id  = json.loads(x.text)
         buffer = ""
         buffer1 = "" 
         if id["response"]["success"] == 42:
             embed=discord.Embed(description="Error - Player not found", color=0xff0000)
             await ctx.send(embed=embed)

             return
         elif id["response"]["success"] == 1:
            stid = id["response"]["steamid"]
            xx = requests.get(f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v1/?key=964A0610CCE27D7155ED1B9E09C32BFE&steamids={stid}")
            xy = requests.get(f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key=964A0610CCE27D7155ED1B9E09C32BFE&steamid={stid}")
            data = json.loads(xx.text)
            gamelist = json.loads(xy.text)
            print(gamelist["response"]["game_count"])
         for i in data["response"]["players"]["player"]:
              print(i)
              time = i["lastlogoff"]
              creation = i["timecreated"]
              lastlogoff = datetime.utcfromtimestamp(int(time))
              timecreated = datetime.utcfromtimestamp(int(creation))
              now = datetime.now()
              years = timecreated.strftime("%Y-%H:%M:%S")
              current_time = now.strftime("%Y-%H:%M:%S")
              start = datetime.strptime(years, "%Y-%H:%M:%S")
              end = datetime.strptime(current_time, "%Y-%H:%M:%S")
              res = (end.year - start.year) * 1 + (end.month - start.month)
              print(res)
         if res == 1:
            buffer1 += "<:steamyears1:1008419109874172064>"
         elif res == 2:
            buffer1 += "<:steamyears2:1008419108259381319>"
         elif res == 3:
            buffer1 += "<:steamyears3:1008419106426474576>"
         elif res == 4:
            buffer1 += "<:steamyears4:1008419105256259614>"
         elif res == 5:
            buffer1 += "<:steamyears5:1008419104107003945>"
         elif res == 6:
            buffer1 += "<:steamyears6:1008419102836150392>"
         if i["personastate"] ==  1:
             buffer += "Online"
         elif i["personastate"] ==  3:
             buffer += "Away"
         elif i["personastate"] == 0:
             buffer += "Offline"
         try:
             i["gameextrainfo"]
             successful = True
         except KeyError:
              cflag = flag.flag(i["loccountrycode"])
              embed1=discord.Embed(title=f"{cflag} {i['personaname']}'s Account:",description=f'`Games:` {gamelist["response"]["game_count"]}\n`Creation Date:` {timecreated} (Age: {res})' , url=i["profileurl"], color=0x80ff80)
              embed1.set_thumbnail(url=f'{i["avatarfull"]}')
              embed1.set_footer(text = "Years of service", icon_url = f"https://steamcommunity-a.akamaihd.net/public/images/badges/02_years/steamyears{res}_80.png")
              embed1.add_field(name="SteamID:", value=f"```fix\n{stid}```", inline=False)
              embed1.add_field(name="Status:", value=f"```ml\n{buffer} ({lastlogoff})```")
              await ctx.reply(embed=embed1)

              return
         if successful:
              cflag = flag.flag(i["loccountrycode"])
              embed1=discord.Embed(title=f"{cflag} {i['personaname']}'s Account:",description=f'`Games:` {gamelist["response"]["game_count"]}\n`Creation Date:` {timecreated} (Age: {res})', url=i["profileurl"], color=0x80ff80)
              embed1.set_thumbnail(url=f'{i["avatarfull"]}')
              embed1.set_footer(text = "Years of service", icon_url = f"https://steamcommunity-a.akamaihd.net/public/images/badges/02_years/steamyears{res}_80.png")
              embed1.add_field(name="SteamID:", value=f"```fix\n{stid}```", inline=False)
              embed1.add_field(name="Status:", value=f"```ml\n{buffer} ({lastlogoff})```")
              embed1.add_field(name="playing:", value=f"```fix\n{i['gameextrainfo']}({i['gameid']})```", inline=False)
         await ctx.reply(embed=embed1)
def setup(client):
     client.add_cog(steam(client))