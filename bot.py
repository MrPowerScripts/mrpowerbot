import discord
from discord.ext import commands
from utils import MOD_ROLE, STREAMER_ROLE
import random
import os

description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='%', description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
@commands.has_role(MOD_ROLE)
async def streamer(ctx, user: discord.Member):
  role = discord.utils.get(user.guild.roles, id=STREAMER_ROLE)
  try:
    if role in user.roles:
      await user.remove_roles(role)
    else:
      await user.add_roles(role)
    ctx.message.add_reaction("✅")
  except Exception as e:
    ctx.message.add_reaction("❌")

@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)

bot.run(os.environ["BOT_TOKEN"])
