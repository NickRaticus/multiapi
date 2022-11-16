import json
from datetime import datetime
from os import devnull
from unicodedata import name
import urllib
import re
import requests
from discord.ext import commands
import discord
import flag
import steamfront
import math
client = steamfront.Client()
auth_token='0e00524d0a0bcd29ac1b49b75e011d21'
from bs4 import BeautifulSoup
class steam(commands.Cog):
    def __init__(self, client):
          self.client = client
    @commands.command()
    async def gameinfo(self, ctx, nameorappid):
         appjson = requests.get(f"https://store.steampowered.com/api/appdetails?appids={nameorappid}&l=english")
         appinfo = json.loads(appjson.text)
         print(appinfo)
         if appinfo != None:
           print(appinfo[f"{nameorappid}"]["data"])
           for x in appinfo[f"{nameorappid}"]["data"]:
            name = x.get("name"[0])
            print(name)
         elif appinfo == None:
             print("name")
             hed = {'Authorization': 'Bearer ' + auth_token}
             xx = requests.get(f"https://www.steamgriddb.com/api/v2/search/autocomplete/{nameorappid}", headers=hed)
             games  = json.loads(xx.text)
             for k, a in enumerate(games["data"]):
               if a["name"]:
                  if 'steam' in a["types"]:
                   gamename =  a["name"]

                   try:
                    game = client.getApp(name=gamename)
                    appid = game.appid
                    print(gamename, appid)
                   except steamfront.errors.AppNotFound:
                     appid = ""
                     pass
                   yx = requests.get(f"https://store.steampowered.com/api/appdetails?appids={appid}&l=english", headers=hed)
                   gamesx  = json.loads(yx.text)
                   print(gamesx)


    @commands.command()
    async def usergame(self, ctx, name, *, message: str):
      x = requests.get(f"http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=964A0610CCE27D7155ED1B9E09C32BFE&vanityurl={name}")
      id  = json.loads(x.text)
      appid = ""
      if id["response"]["success"] == 42:
             embed=discord.Embed(description="Error - User not found", color=0xff0000)
             await ctx.send(embed=embed)
      elif id["response"]["success"] == 1:
             buffer10 = ""
             stid = id["response"]["steamid"]
             hed = {'Authorization': 'Bearer ' + auth_token}
             xx = requests.get(f"https://www.steamgriddb.com/api/v2/search/autocomplete/{message}", headers=hed)
             games  = json.loads(xx.text)
             print(games)
             buffer13 = ""
             numb = int(0)
             ach = int(0)
             stat = int(0)
             ach_ach = ""
             ach_acch = ""
             ach_not = ""
             ach_list = ""
             ach_notac = ""
             hgnames = ""
             achlp_succ = ""
             all_achievements = []
             player_achievements = []
             lpnames = ""
             for k, a in enumerate(games["data"]):
               if a["name"]:
                  if 'steam' in a["types"]:
                   gamename =  a["name"]

                   try:
                    game = client.getApp(name=gamename)
                    appid = game.appid
                    print(gamename, appid)
                   except steamfront.errors.AppNotFound:
                     appid = ""
                     pass
                   xy = requests.get(f"https://api.steampowered.com/Iplayerservice/Getownedgames/v0001/?key=964A0610CCE27D7155ED1B9E09C32BFE&steamid={stid}")
                   usergames  = json.loads(xy.text)
                   if usergames["response"] == {}:
                     embed=discord.Embed(description="Error - User has privated their library.", color=0xff0000)
                     await ctx.send(embed=embed)
                   for t, p in enumerate(usergames["response"]["games"]):
                    if appid:
                      if p["appid"] == appid:

                         numb = numb+1
                         devlink = ""
                         pcrec = ""
                         buffer14 = ""
                         try:
                          p['playtime_2weeks']
                          buffer13 = f"\nRecent: {p['playtime_2weeks']//60}h"
                          if p['playtime_2weeks']//60 < 1:
                           buffer13 = f"\nRecent: <1h"
                         except KeyError:
                           buffer13 = ""
                           pass
                         buffer14 = f"All-time: {p['playtime_forever']//60}h"
                         if p['playtime_forever']/60 == 0:
                            buffer14 = "All-time: 0h"  
                         elif p['playtime_forever']//60 < 1:
                            buffer14 = "All-time: <1h"

                         buffer10 = f"{buffer14}{buffer13}"
                         xz = requests.get(f"https://store.steampowered.com/api/appdetails?appids={appid}&l=english")
                         rx = requests.get(f"http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid={appid}&key=964A0610CCE27D7155ED1B9E09C32BFE&steamid={stid}")
                         cx = requests.get(f"https://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v2?gameid={appid}")
                         game_progress = json.loads(rx.text)
                         all_ach = json.loads(cx.text)
                         try:
                          for hg in (all_ach["achievementpercentages"]["achievements"]):
                              if hg["name"]:
                               hgnames = f"{hg['name']} {math.trunc(hg['percent'])}%"
                               procent = "%"
                               all_achievements += [hgnames]                        
                              for lp in (game_progress["playerstats"]["achievements"]):
                               
                               if lp["name"]:
                                  ach_ach = f"{lp['name']} {math.trunc(hg['percent'])}%"
                             
                               if lp["name"]:
                                player_achievements += [ach_ach]                             
                               #if hg['name']: 
                                
                                #ach_list += f"{lp['name']} "
                                #ach_list = re.sub(" (?=.*\ )", "|", ach_list)
                                #ach_not = re.sub(ach_list, "", hgnames)
                                #ach_notac = ach_not
                                #ach_notac = re.sub('.*\B.\d\B..', '', ach_notac)
                                #ach_notac = re.sub('^ ', '', ach_notac)
                                #ach_notac = re.sub('%', '% \n', ach_notac)
                                #ach_notac = re.sub('\s +', '\n', ach_notac)
                               
                             
                            
                         except KeyError:
                           ("pass ach")
                           pass
                         try:
                              for jk, lp in enumerate(game_progress["playerstats"]["achievements"]):
                                 if lp["name"]:
                                    ach_acch += f"{lp['name']} {math.trunc(hg['percent'])}%\n"
                                    ach = ach+1
                         except KeyError:
                            pass
                         try:
                           for ko, lo in enumerate(game_progress["playerstats"]["stats"]):
                             stat = stat+1
                             print(stat)
                         except KeyError:
                           print("stat faild")
                         gameinfo = json.loads(xz.text) 
                         dev = re.compile(r"[[''\]]")
                         devf = re.sub(dev, '', str(gameinfo[f"{appid}"]["data"]["developers"]))
                         pubf = re.sub(dev, '', str(gameinfo[f"{appid}"]["data"]["publishers"]))
                         buffer11 = ""
                         r = requests.get(f'https://store.steampowered.com/app/{appid}')
                         soup = BeautifulSoup(r.content, 'html.parser')
                         s = soup.find('div', id= 'developers_list')
                         g = soup.find_all('div', {"class":"dev_row"})
                         pubu = str(g[1])
                         devfind = s('a')
                         for publink in pubu:
                          pubmatch = re.compile('href=\"\S+.*\"')
                          o = pubmatch.findall(pubu)
                          pubmatch = re.compile('href')
                          o = re.sub(pubmatch, '', str(o))
                          pubmatch = re.compile('"')
                          o = re.sub(pubmatch, '', o)
                          pubmatch = re.compile("'")
                          o = re.sub(pubmatch, '', o)
                          pubmatch = re.compile("\[")
                          o = re.sub(pubmatch, '', o)
                          pubmatch = re.compile("]")
                          o = re.sub(pubmatch, '', o)
                          pubmatch = re.compile("=")
                          o = re.sub(pubmatch, '', o)
                          pubmatch = re.compile("\?.*")
                          o = re.sub(pubmatch, '', o)                            
                         for devlink in devfind:
                          devlink = devlink.get('href')
                          devlink = re.sub('\?.*', "", devlink)
                         buffer12 = ""
                         d = requests.get(f'{devlink}')
                         m = requests.get(f'{o}')
                         pubhtml = BeautifulSoup(m.content, 'html.parser')
                         for m in pubhtml.select('div.curator_avatar_image'):
                             for l in m.select('img'):
                              buffer12 += l['src']
                              print(buffer12)
                         devhtml = BeautifulSoup(d.content, 'html.parser')

                         for d in devhtml.select('div.curator_avatar_image'):
                             for i in d.select('img'):
                              buffer11 += i['src']
                              print(buffer11)
                         price = ""
                         try:
                           gameinfo[f'{appid}']['data']['price_overview']['final_formatted']
                           price = gameinfo[f'{appid}']['data']['price_overview']['final_formatted']
                           print(price)
                         except KeyError:
                            price = "Couldn't be found."
                            print(price)
                         
                         try:
                            if p["rtime_last_played"] == 0:
                              days = "Never played"
                            else:
                             last_played = datetime.utcfromtimestamp(p["rtime_last_played"])
                             now = datetime.now()
                             played = last_played.strftime("%Y-%m-%d %H:%M:%S")
                             current_time = now.strftime("%Y-%m-%d %H:%M:%S")
                             start = datetime.strptime(played, "%Y-%m-%d %H:%M:%S")
                             end = datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S")
                             res = end - start
                             print(res.days)
                             days = res.days
                             
                             if days == 0:
                                days = f"{last_played} (today)"
                             elif days > 0:
                                days = f"{last_played} ({days} days ago)"
                            print(days)
                         except KeyError:
                              print("test")
                         try:
                            incomplete = [x for x in all_achievements if x not in player_achievements]
                            complete = [x for x in all_achievements if x in player_achievements]
                            incopstr = ''
                            completestr = ''
                            for x in complete:
                              completestr += x + '\n'
                            for x in incomplete:
                              incopstr += x + '\n'

                         except KeyError:
                           pass
                         embed1=discord.Embed(title=f"{gamename}", description=f"`appid:`{appid}\n`Type:`{gameinfo[f'{appid}']['data']['type']}\n`Price:`{price}", color=0x80ff80)
                         embed1.set_thumbnail(url=f'{gameinfo[f"{appid}"]["data"]["header_image"]}')
                         try:
                          embed1.add_field(name="Playtime:", value=f'```{buffer10}```', inline=False)
                          embed1.add_field(name="Last played:", value=f"```{days}```")
                         except KeyError:
                           pass
                         try:
                           total_ach = gameinfo[f'{appid}']['data']["achievements"]["total"]
                           embed1.add_field(name="Achievements:", value=f"```Completion {ach}/{total_ach}```")
                           embed1.add_field(name="‎", value="‎", inline=True)
                           embed1.add_field(name="Complete Achievements",value=f"```{completestr}```", inline=True)
                           embed1.add_field(name="Incomplete Achievements",value=f"```{incopstr}```", inline=True)

                           print(ach_notac)
                           print(ach_ach)
                         except KeyError:
                           print("stach")

                         try:
                          embed1.set_author(name=f"{devf}", url=gameinfo[f'{appid}']['data']['support_info']['url'], icon_url=buffer11)
                         except KeyError:
                           pass
                         try:
                          embed1.set_footer(text = f'{pubf} - {gameinfo[f"{appid}"]["data"]["release_date"]["date"]}', icon_url=f"{buffer12}")
                         except KeyError:
                           pass
                         await ctx.send(embed=embed1)
                         print(f"{numb}\nname:{name}\nmessage: {message}\ngames:{gamename}\nplaytime:\n{buffer10}")
                         player_achievements = []
                         all_achievements = []
                         if ach != int(0):
                           ach = int(0)
             if numb == int(0):
                           embed=discord.Embed(description="Error - User has none of the mentioned games.", color=0xff0000)
                           await ctx.send(embed=embed)

    @commands.command()
    async def stfriends(self, ctx, name):
      friendpro = ""
      friendcount = int(0)
      extrafriend = ""
      x = requests.get(f"http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=964A0610CCE27D7155ED1B9E09C32BFE&vanityurl={name}")
      id  = json.loads(x.text)
      if id["response"]["success"] == 42:
             embed=discord.Embed(description="Error - User not found", color=0xff0000)
             await ctx.send(embed=embed)
      elif id["response"]["success"] == 1:
         stid = id["response"]["steamid"]
         xy = requests.get(f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v1/?key=964A0610CCE27D7155ED1B9E09C32BFE&steamids={stid}")
         prosum = json.loads(xy.text)
         friendget = requests.get(f"https://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=964A0610CCE27D7155ED1B9E09C32BFE&steamid={stid}&relationship=friend")
         f = json.loads(friendget.text)
         friend3 = ""
         friend4 = ""
         friend5 = ""
         print(f["friendslist"]["friends"])
         for info in prosum["response"]["players"]["player"]:
            nameuser = info["personaname"]
         for friend, item in enumerate(f["friendslist"]["friends"]):
          if item["steamid"]:
            friendcount  = friendcount + 1
         for friend, item in enumerate(f["friendslist"]["friends"][:50]):
          if item["steamid"]:
            xx = requests.get(f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key=964A0610CCE27D7155ED1B9E09C32BFE&steamids={item['steamid']}")
            sum = json.loads(xx.text)
            sinceraw = datetime.utcfromtimestamp(int(item["friend_since"]))
            since = sinceraw.strftime("%Y-%d-%M")
            
            for i in (sum["response"]["players"]):
               embed1=discord.Embed(title=f"{nameuser}'s friends", description=f"`Amount of friends:` {friendcount}")
          
            if 0 <= friend <= 10:
                  friendpro += f'```{i["personaname"]} Since:{since}```'
            elif 10 <= friend <=20:
                  extrafriend += f'```{i["personaname"]} Since:{since}```'
            elif 20 <= friend <= 30:
                  friend3 += f'```{i["personaname"]} Since:{since}```'
            elif 30 <= friend <= 40:
                  friend4 += f'```{i["personaname"]} Since:{since}```'
            elif 40 <= friend <= 50:
                friend5 += f'```{i["personaname"]} Since:{since}```'
                  




      print(friendcount)
      if 0 <= friendcount <= 10:
         embed1.add_field(name="Friends:", value=friendpro, inline=False)
      if 10 <= friendcount <= 20:
         embed1.add_field(name="Friends:", value=friendpro, inline=False)
         embed1.add_field(name="‎", value=extrafriend, inline=False)

      if 20 <= friendcount <= 30:
         embed1.add_field(name="Friends:", value=friendpro, inline=False)
         embed1.add_field(name="‎", value=extrafriend, inline=False)
         embed1.add_field(name="‎", value=friend3, inline=False)
      if 30 <= friendcount <= 40:
         embed1.add_field(name="Friends:", value=friendpro, inline=False)
         embed1.add_field(name="‎", value=extrafriend, inline=False)
         embed1.add_field(name="‎", value=friend3, inline=False)
         embed1.add_field(name="‎", value=friend4, inline=False)
      if 40 <= friendcount <= 50:
         embed1.add_field(name="Friends:", value=friendpro, inline=False)
         embed1.add_field(name="‎", value=extrafriend, inline=False)
         embed1.add_field(name="‎", value=friend3, inline=False)
         embed1.add_field(name="‎", value=friend4, inline=False)
         embed1.add_field(name="‎", value=friend5, inline=False)

      if friendcount > 50:
         embed1.add_field(name="Friends:", value=friendpro, inline=False)
         embed1.add_field(name="‎", value=extrafriend, inline=False)
         embed1.add_field(name="‎", value=friend3, inline=False)
         embed1.add_field(name="‎", value=friend4, inline=False)
         embed1.add_field(name="‎", value=friend5, inline=False)
         friendlimit = f"User has {friendcount-50} friends which remain to be shown due to limitions."
         embed1.add_field(name="Notice:", value=f"[{friendlimit}](https://steamcommunity.com/id/{name}/friends/)", inline=False)
      await ctx.send(embed=embed1)
      print(friendpro)


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
async def setup(client):
    await client.add_cog(steam(client))