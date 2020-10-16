import discord
import os
from discord.ext import commands

prefix=';'
description = '''An example bot to showcase the discord.ext.commands extension
module. There are a number of utility commands being showcased here.'''
client = discord.Client()
bot = commands.Bot(command_prefix=prefix, description=description)

initial_extensions = ['cogs.main']

# retired cogs
# 'cogs.monsters.monsters', 

for extension in initial_extensions:
    bot.load_extension(extension)

bot.run(os.environ["BOT_TOKEN"])
