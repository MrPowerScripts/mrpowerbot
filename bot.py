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

description = '''An example bot to showcase the discord.ext.commands extension
module. There are a number of utility commands being showcased here.'''
client = discord.Client()
bot = commands.Bot(command_prefix='%', description=description)

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

@bot.event
async def on_raw_reaction_add(payload):
  print(payload)
  print(payload.channel_id)
  channel = discord.utils.get(bot.get_all_channels(), id=payload.channel_id)
  print(channel)
  message = await channel.fetch_message(payload.message_id)
  print(message)
  receiver = message.author.id
  print(receiver)
  if receiver == payload.user_id:
    print("emoji from author")
  # else:
  #   db.zap(message.author.id)
  #   print("zapped!")
  # if reaction.emoji == '⚡':
  #   if reaction.event_type == 'REACTION_ADD'
  #     if reaction.
  #     db.zap(user.id)
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


bot.run(os.environ["BOT_TOKEN"])
