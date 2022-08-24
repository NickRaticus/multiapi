from http import client
import discord

import os

import re

from discord.ext import commands

from discord.ext import tasks
import asyncio
from mojang import MojangAPI
intents = discord.Intents().all()
client = discord.Client(intents=intents)
intents.message_content = True
bot = commands.Bot(command_prefix=('api?'), intents=intents)


async def load_extensions():
 for f in os.listdir("./cogs"):
    if f.endswith(".py"):
        await bot.load_extension(f"cogs.{f[:-3]}")

async def main():
    async with bot:
        await load_extensions()
        await bot.start('OTY2NzQwNTM2ODgwOTQ3MjIw.G140NL.OxDRR__wgb7YbQyvLVwXu67tVBmsQ5Ya6Dj_qY')

asyncio.run(main())
