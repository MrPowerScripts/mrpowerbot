import discord
from discord.ext import commands
from utils import (
  MOD_ROLE, 
  STREAMER_ROLE, 
  LOG_CHANNEL,
  REVISION,
)
import db
import random
import os

prefix=';'
description = '''An example bot to showcase the discord.ext.commands extension
module. There are a number of utility commands being showcased here.'''
client = discord.Client()
bot = commands.Bot(command_prefix=prefix, description=description)

@bot.event
async def on_ready():
  print('Logged in as')
  db.preparedb()
  log_channel = discord.utils.get(bot.get_all_channels(), id=LOG_CHANNEL)
  await log_channel.send(f"HELLO WORLD! I'm MrPowerBot@{REVISION}")
  try:
    version = db.status_check()
    await log_channel.send(f"I'm connected to Postgres! {version}")
  except:
    await log_channel.send(f"Posrgres connection failed 😭😭😭")
  print(bot.user.name)
  print(bot.user.id)
  print('------')

# @bot.event
# async def on_message(message):
#   if bot.user.mentioned_in(message) and message.mention_everyone is False:
#     await message.channel.send(f"hello! I'm awake! `{prefix}help` for help")

@bot.event
async def on_raw_reaction_add(payload):
  print(payload)
  channel = discord.utils.get(bot.get_all_channels(), id=payload.channel_id)
  message = await channel.fetch_message(payload.message_id)
  receiver = message.author.id
  if receiver == payload.user_id:
    print("emoji from author")
  else:
    if payload.emoji == '⚡':
      if payload.event_type == 'REACTION_ADD':
        db.zap(receiver)
        print("zapped!")

    #do stuff

@bot.command()
@commands.has_role(MOD_ROLE)
async def streamer(ctx, user: discord.Member):
  role = discord.utils.get(user.guild.roles, id=STREAMER_ROLE)
  try:
    if role in user.roles:
      await user.remove_roles(role)
      await ctx.message.add_reaction("❎")
    else:
      await user.add_roles(role)
      await ctx.message.add_reaction("✅")
  except Exception as e:
    await ctx.message.add_reaction("❌")

@bot.command()
async def add(ctx, left: int, right: int):
  """Adds two numbers together."""
  await ctx.send(left + right)

@bot.command()
async def register(ctx):
  user_id = ctx.message.author.id
  print(f"registering {user_id}")
  db.register_user(user_id)

@bot.command()
async def zaps(ctx):
  print(f"zaps {ctx.message.author.name}")
  zaps = db.zaps(ctx.message.author.id)
  ctx.message.send(f"{ctx.message.author.name}: {str(zaps)}")

bot.run(os.environ["BOT_TOKEN"])
