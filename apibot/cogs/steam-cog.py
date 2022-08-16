import json
from datetime import datetime
import urllib
import re
import requests
from discord.ext import commands
import discord
import flag
class steam(commands.Cog):
    def __init__(self, client):
          self.client = client 
    @commands.command()
    async def strecent(self, ctx, name):
         buffer3 = ""
         x = requests.get(f"http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=964A0610CCE27D7155ED1B9E09C32BFE&vanityurl={name}")
         id  = json.loads(x.text)
         if id["response"]["success"] == 42:
             embed=discord.Embed(description="Error - User not found", color=0xff0000)
             await ctx.send(embed=embed)
         elif id["response"]["success"] == 1:
            stid = id["response"]["steamid"]
            zc =requests.get(f"https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key=964A0610CCE27D7155ED1B9E09C32BFE&steamid={stid}")
            xx = requests.get(f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v1/?key=964A0610CCE27D7155ED1B9E09C32BFE&steamids={stid}")
            sum = json.loads(xx.text)
            recentplay = json.loads(zc.text)
         for i in sum["response"]["players"]["player"]:
            print(i["personaname"])
         if recentplay["response"] == {}:
            embed=discord.Embed(description="Error - User has set their Game details to private or friends only.", color=0xff0000)
            await ctx.send(embed=embed)
         elif recentplay["response"]["total_count"] == 0:
            embed=discord.Embed(description="Error - User has not played a game within the last two weeks.", color=0xff0000)
            await ctx.send(embed=embed)
            print(recentplay["response"])
         try:
            recentplay["response"]["games"]
            playsucc = True
         except KeyError:
            return
         if playsucc:

            for index, item in enumerate(recentplay["response"]["games"]):
                if item["appid"]:
                  buffer3 += f'```{item["name"]}\nRecent playtime: {item["playtime_2weeks"]//60}\nPlaytime forever: {item["playtime_forever"]//60}```'
            embed1=discord.Embed(title=f"{i['personaname']}'s Recently played games", description=f"`Amount recently played:` {recentplay['response']['total_count']}")
            embed1.add_field(name="Recently played:", value=buffer3)
            await ctx.send(embed=embed1)
    @commands.command()
    async def stprofile(self, ctx, name):
         x = requests.get(f"http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=964A0610CCE27D7155ED1B9E09C32BFE&vanityurl={name}")
         id  = json.loads(x.text)
         buffer = ""
         buffer1 = "" 
         buffer2 = ""
         if id["response"]["success"] == 42:
             embed=discord.Embed(description="Error - User not found\n\n**Description:** Sends a overall detailed embed of a steam profile.\n\n\n**Usage:**\napi?stprofile <Vanity-url>\n**Example:**\napi?stprofile xDeerz", color=0xff0000)
             await ctx.send(embed=embed)
             return
         elif id["response"]["success"] == 1:
            stid = id["response"]["steamid"]
            xx = requests.get(f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v1/?key=964A0610CCE27D7155ED1B9E09C32BFE&steamids={stid}")
            xy = requests.get(f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key=964A0610CCE27D7155ED1B9E09C32BFE&steamid={stid}")   
            xz = requests.get(f"https://api.steampowered.com/IPlayerService/GetSteamLevel/v1/?key=964A0610CCE27D7155ED1B9E09C32BFE&steamid={stid}")
            zc = requests.get(f"https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key=964A0610CCE27D7155ED1B9E09C32BFE&steamid={stid}")
            getlevel = json.loads(xz.text)
            data = json.loads(xx.text)
            gamelist = json.loads(xy.text)
            recentplay = json.loads(zc.text)
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
              recentsucc = ""

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
            recentplay["response"]["games"]
            recentsucc = True
         except KeyError:
            buffer2 = "Playing activity on this profile is set to private "
         if recentsucc:
            for index, item in enumerate(recentplay["response"]["games"][:3]):
                if item["appid"]:

                  buffer2 += f'```{item["name"]}\nRecent playtime: {item["playtime_2weeks"]//60}\nPlaytime forever: {item["playtime_forever"]//60}```'
         if recentsucc:
          buffer2 += f"Use `api?strecent {name}` for more details"
         try:
             i["gameextrainfo"]
             successful = True
         except KeyError:
              cflag = flag.flag(i["loccountrycode"])
              embed1=discord.Embed(title=f"{cflag} {i['personaname']}'s Account:",description=f'`Games:` {gamelist["response"]["game_count"]}\n`Creation Date:` {timecreated} (Age: {res})\n`Level:` {getlevel["response"]["player_level"]}\n`SteamID:` {stid}' , url=i["profileurl"], color=0x80ff80)
              embed1.set_thumbnail(url=f'{i["avatarfull"]}')
              embed1.set_footer(text = "Years of service", icon_url = f"https://steamcommunity-a.akamaihd.net/public/images/badges/02_years/steamyears{res}_80.png")
              embed1.add_field(name="Status:", value=f"```ml\n{buffer} ({lastlogoff})```")
              embed1.add_field(name="Recently played", value=buffer2, inline=False)

              await ctx.reply(embed=embed1)

              return
         if successful:
              cflag = flag.flag(i["loccountrycode"])
              embed1=discord.Embed(title=f"{cflag} {i['personaname']}'s Account:",description=f'`Games:` {gamelist["response"]["game_count"]}\n`Creation Date:` {timecreated} (Age: {res})\n`Level:` {getlevel["response"]["player_level"]}\n`SteamID:` {stid}', url=i["profileurl"], color=0x80ff80)
              embed1.set_thumbnail(url=f'{i["avatarfull"]}')
              embed1.set_footer(text = "Years of service", icon_url = f"https://steamcommunity-a.akamaihd.net/public/images/badges/02_years/steamyears{res}_80.png")
              embed1.add_field(name="Status:", value=f"```ml\n{buffer} ({lastlogoff})```")
              embed1.add_field(name="Recently played", value=buffer2, inline=False)
              embed1.add_field(name="playing:", value=f"```fix\n{i['gameextrainfo']}({i['gameid']})```", inline=False)
         await ctx.reply(embed=embed1)
def setup(client):
     client.add_cog(steam(client))