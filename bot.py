import discord
import asnycio
from discord.ext import commands
from utils import (
  MOD_ROLE, 
  STREAMER_ROLE, 
  LOG_CHANNEL,
  ROUNDTABLE_ROLE,
  REVISION,
  MRPS_GUILD,
)
import db
import random
import os
import sys

prefix=';'
description = '''An example bot to showcase the discord.ext.commands extension
module. There are a number of utility commands being showcased here.'''
client = discord.Client()
bot = commands.Bot(command_prefix=prefix, description=description)

@bot.event
async def on_ready():

  print(bot.guilds)
  for guild in bot.guilds:
    if guild.id != MRPS_GUILD:
      print(f"leaving: {guild.name}")
      await guild.leave()

  print('Logged in as')
  db.preparedb()
  log_channel = discord.utils.get(bot.get_all_channels(), id=LOG_CHANNEL)
  await log_channel.send(f"HELLO WORLD! I'm MrPowerBot@{REVISION}")
  try:
    version = db.status_check()
    await log_channel.send(f"`I'm connected to Postgres! {version}`")
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
  receiver = message.author
  if receiver == payload.user_id:
    print("emoji from author")
  else:
    print("checking if zap")
    print(f"emoji is: {payload.emoji}")
    if str(payload.emoji) == "⚡":
      print("is zap. checking add")
      if payload.event_type == 'REACTION_ADD':
        print(f"is add, going to zap {receiver}")
        db.zap(receiver)
        print("zapped!")

@bot.event
async def on_raw_reaction_remove(payload):
  print(payload)
  channel = discord.utils.get(bot.get_all_channels(), id=payload.channel_id)
  message = await channel.fetch_message(payload.message_id)
  receiver = message.author
  if receiver == payload.user_id:
    print("emoji from author")
  else:
    print("checking if zap")
    print(f"emoji is: {payload.emoji}")
    if str(payload.emoji) == "⚡":
      print("is zap. checking remove")
      if payload.event_type == 'REACTION_REMOVE':
        print(f"is remove, going to remove zap from {receiver}")
        db.zap(receiver, remove=True)
        print("zapped!")

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
@commands.has_role(MOD_ROLE)
async def roundtable(ctx, user: discord.Member):
  role = discord.utils.get(user.guild.roles, id=ROUNDTABLE_ROLE)
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
@commands.has_role(MOD_ROLE)
async def reboot(ctx):
  await ctx.channel.send(f"restarting bot")
  sys.exit()

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
  await ctx.message.channel.send(f"{ctx.message.author.name}: {str(zaps)}")

@bot.command()
async def zapleaders(ctx):
  zaps = db.zap_leaders()
  print(zaps)
  message = '\n'.join(map(str, zaps))

  await ctx.message.channel.send(f"{message}")

async def monsters():
    await bot.wait_until_ready()
    counter = 0
    channel = discord.Object(id='')
    while not bot.is_closed:
        counter += 1
        # await bot.send_message(channel, counter)
        print(counter)
        await asyncio.sleep(10) # task runs every 60 seconds

bot.loop.create_task(monsters())

bot.run(os.environ["BOT_TOKEN"])
