import discord

import os

import re

from discord.ext import commands

from discord.ext import tasks

from mojang import MojangAPI

bot = discord.Client()
bot = commands.Bot(command_prefix=('api?'))


for f in os.listdir("./cogs"):
    if f.endswith(".py"):
     bot.load_extension("cogs." + f[:-3])


bot.run("MTAwNTIxNzQ5MjQ3NTU3NjM5MA.Gs0Y8h.NsGXQl8S6unMN3-Cp7f6cHAeqJwNDSCLSgTzXg")