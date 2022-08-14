from discord.ext import commands
import discord
from mojang import MojangAPI
from datetime import datetime
import json 
import urllib
import requests


class mc(commands.Cog):
    def __init__(self, client):
          self.client = client 
    @commands.command()
    async def uuid(self, ctx, name):
        uuid = MojangAPI.get_uuid(name)
        if uuid == None:
             embed=discord.Embed(description="Error - Player not found", color=0xff0000)
             await ctx.send(embed=embed)
        else:
             embed=discord.Embed(description=f"``{uuid}``")
             await ctx.send(embed=embed)
    @commands.command()
    async def skin(self, ctx, name):
        uuid = MojangAPI.get_uuid(name)
        if uuid == None:
            embed=discord.Embed(description="Error - Player not found", color=0xff0000)
            await ctx.send(embed=embed)
        if uuid:
            embed1=discord.Embed(color=0x00ff00)
            embed1.set_image(url = f"https://crafatar.com/renders/body/{uuid}?scale=10&overlay")
            await ctx.reply(embed=embed1)
    @commands.command()
    async def lookup(self, ctx, username):
        uuid = MojangAPI.get_uuid(username)
        if uuid == None:
             embed=discord.Embed(description="Error - Player not found", color=0xff0000)
             await ctx.send(embed=embed)
        name_history = MojangAPI.get_name_history(uuid)
        name_history.reverse()
        buffer = ""
        for index, item in enumerate(name_history):
          time = item['changed_to_at']
          datetime_obj = datetime.utcfromtimestamp(int(time/1000))
          if item['changed_to_at'] == 0:  
           buffer += (f"[{item['name']}][First]\n")
          elif uuid:
                 buffer += (f"[{item['name']}][{datetime_obj}]\n")
          embed=discord.Embed(title="", description=f"```md\n{buffer}```", color=0x80ff80)
        await ctx.reply(embed=embed)
    @commands.command()
    async def mcprofile(self, ctx, username):
         uuid = MojangAPI.get_uuid(username)
         if uuid == None:
              embed=discord.Embed(description="Error - Player not found", color=0xff0000)
              await ctx.send(embed=embed)
         name_history = MojangAPI.get_name_history(uuid)
         profile = MojangAPI.get_profile(uuid)
         name_history.reverse()
         buffer = ""
         buffer1 = ""
         for index, item in enumerate(name_history[:5]):
            time = item['changed_to_at']
            datetime_obj = datetime.utcfromtimestamp(int(time/1000))
            if item['changed_to_at'] == 0:  
                buffer += (f"[{item['name']}][First]\n")
            elif index == 0:
                buffer += ""  
            elif uuid:
                buffer += (f"[{item['name']}][{datetime_obj}]\n")
            elif profile.is_legacy_profile:
                buffer1 += ("`This is a legacy account`")
            embed1=discord.Embed(title=f"{username}'s Account:", description=f"{buffer1}", color=0x80ff80)
            embed1.set_thumbnail(url=f"https://crafatar.com/renders/body/{uuid}?scale=10&overlay")
            embed1.add_field(name="UUID:", value=f"`{uuid}`", inline=False)
            embed1.add_field(name="Recent Names:", value=f"```md\n{buffer}``` Use ``?lookup {username}`` for more details.", inline=False)
         await ctx.reply(embed=embed1)
    @commands.command()
    async def server(self, ctx, address):
         xx = requests.get(f"https://api.mcsrvstat.us/2/{address}")
         serverInfo1 = json.loads(xx.text)
         x = requests.get(f"https://eu.mc-api.net/v3/server/ping/{address}")
         serverInfo = json.loads(x.text)
         buffer = ""
         try:
           serverInfo["cache"]
         except KeyError:
            embed=discord.Embed(title="Minecraft Server:")
            embed.add_field(name="Error:", value="Server is either offline or an exception was created.", inline=True)
            await ctx.send(embed=embed)
         if serverInfo["players"]["online"] == 0:
            embed=discord.Embed(title="Minecraft Server:")
            embed.add_field(name="ip:", value=address, inline=True)
            embed.add_field(name="Port:", value=serverInfo1["port"], inline=True)
            embed.add_field(name="‎", value="‎", inline=True)
            embed.add_field(name="Player Count:", value=f'{serverInfo["players"]["online"]}/{serverInfo["players"]["max"]}', inline=True)
            embed.add_field(name="Version", value=serverInfo["version"]["name"], inline=True)
            embed.add_field(name="Players", value="0 players are online.", inline=False)
            embed.set_thumbnail(url=f"https://mc-api.net/v3/server/favicon/{address}") 
            await ctx.send(embed=embed)
            return
         try:
             serverInfo["players"]["sample"]
             successful = True
         except KeyError:
              embed=discord.Embed(title="Minecraft Server:")
              embed.add_field(name="ip:", value=address, inline=True)
              embed.add_field(name="Port:", value=serverInfo1["port"], inline=True)
              embed.add_field(name="‎", value="‎", inline=True)
              embed.add_field(name="Player Count:", value=f'{serverInfo["players"]["online"]}/{serverInfo["players"]["max"]}', inline=True)
              embed.add_field(name="Version", value=serverInfo["version"]["name"], inline=True)
              embed.add_field(name="Players", value="Playerlist is private.", inline=False)
              embed.set_thumbnail(url=f"https://mc-api.net/v3/server/favicon/{address}")
              await ctx.send(embed=embed)
              return
         if successful:
             if serverInfo["players"]["sample"] == [] or "§":
              embed=discord.Embed(title="Minecraft Server:")
              embed.add_field(name="ip:", value=address, inline=True)
              embed.add_field(name="Port:", value=serverInfo1["port"], inline=True)
              embed.add_field(name="‎", value="‎", inline=True)
              embed.add_field(name="Player Count:", value=f'{serverInfo["players"]["online"]}/{serverInfo["players"]["max"]}', inline=True)
              embed.add_field(name="Version", value=serverInfo["version"]["name"], inline=True)
              embed.add_field(name="Players", value="Playerlist is private.", inline=False)
              embed.set_thumbnail(url=f"https://mc-api.net/v3/server/favicon/{address}")
              await ctx.send(embed=embed)
              return
         for index, item in enumerate(serverInfo["players"]["sample"]):
             if item["name"] == "xDeerz":  
               buffer += (f'```ansi\n[101m {item["name"]}```')
             if item["name"]:
               buffer += (f'```fix\n{item["name"]}```')
        
             embed=discord.Embed(title="Minecraft Server:")
             embed.add_field(name="ip:", value=address, inline=True)
             embed.add_field(name="Port:", value=serverInfo1["port"], inline=True)
             embed.add_field(name="‎", value="‎", inline=True)
             embed.add_field(name="Player Count:", value=f'{serverInfo["players"]["online"]}/{serverInfo["players"]["max"]}', inline=True)
             embed.add_field(name="Version", value=serverInfo["version"]["name"], inline=True)
             embed.add_field(name="Players", value=buffer, inline=False)
             embed.set_thumbnail(url=f"https://mc-api.net/v3/server/favicon/{address}") 
         await ctx.send(embed=embed)
    
def setup(client):
     client.add_cog(mc(client))