from discord.ext import commands
import discord
import asyncio
import datetime
import random
import os
import sys
import db
from utils import (
  MOD_ROLE, 
  STREAMER_ROLE, 
  LOG_CHANNEL,
  ROUNDTABLE_ROLE,
  REVISION,
  MRPS_GUILD,
  MRPSTY_CHANNEL
)

class Main(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):

    print(self.bot.guilds)
    for guild in self.bot.guilds:
      if guild.id != MRPS_GUILD:
        print(f"leaving: {guild.name}")
        await guild.leave()

    print('Logged in as')
    db.preparedb()
    log_channel = discord.utils.get(self.bot.get_all_channels(), id=LOG_CHANNEL)
    await log_channel.send(f"HELLO WORLD! I'm MrPowerself.bot@{REVISION}")
    try:
      version = db.status_check()
      await log_channel.send(f"`I'm connected to Postgres! {version}`")
    except:
      await log_channel.send(f"Posrgres connection failed 😭😭😭")
    print(self.bot.user.name)
    print(self.bot.user.id)
    print('------')

  @commands.Cog.listener()
  async def on_message(self, message):
    # print(message)
    if message.channel.id == MRPSTY_CHANNEL:
      print("in mrps ty channel")
      if message.content != "ok":
        print("this is not ok")
        await message.delete()

  @commands.Cog.listener()
  async def on_raw_reaction_add(self, payload):
    print(payload)
    channel = discord.utils.get(self.bot.get_all_channels(), id=payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    receiver = message.author
    msg_created = message.created_at.timestamp()
    current_time = datetime.datetime.now().timestamp()
    time_limit = datetime.datetime.now().timestamp() - 600
    print(f"message created: {msg_created}")
    print(f"current time: {current_time}")
    print(f"time limit: {time_limit}")
    if receiver.id == payload.user_id:
      print("emoji from author")
    elif msg_created <= time_limit:
      print("message too old")
    else:
      print("checking if zap")
      print(f"emoji is: {payload.emoji}")
      if str(payload.emoji) == "⚡":
        print("is zap. checking add")
        if payload.event_type == 'REACTION_ADD':
          print(f"is add, going to zap {receiver}")
          db.zap(receiver)
          print("zapped!")

  @commands.Cog.listener()
  async def on_raw_reaction_remove(self, payload):
    print(payload)
    channel = discord.utils.get(self.bot.get_all_channels(), id=payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    receiver = message.author
    msg_created = message.created_at.timestamp()
    current_time = datetime.datetime.now().timestamp()
    time_limit = datetime.datetime.now().timestamp() - 10
    print(f"message created: {msg_created}")
    print(f"current time: {current_time}")
    print(f"time limit: {time_limit}")
    if receiver.id == payload.user_id:
      print("emoji from author")
    elif msg_created <= time_limit:
      print("message too old")
    else:
      print("checking if zap")
      print(f"emoji is: {payload.emoji}")
      if str(payload.emoji) == "⚡":
        print("is zap. checking remove")
        if payload.event_type == 'REACTION_REMOVE':
          print(f"is remove, going to remove zap from {receiver}")
          db.zap(receiver, remove=True)
          print("zapped!")

  @commands.command()
  @commands.has_role(MOD_ROLE)
  async def streamer(self, ctx, user: discord.Member):
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

  @commands.command()
  @commands.has_role(MOD_ROLE)
  async def roundtable(self, ctx, user: discord.Member):
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

  @commands.command()
  @commands.has_role(MOD_ROLE)
  async def reboot(self, ctx):
    await ctx.channel.send(f"restarting self.bot")
    sys.exit()

  @commands.command()
  async def add(self, ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)

  @commands.command()
  async def register(self, ctx):
    user_id = ctx.message.author.id
    print(f"registering {user_id}")
    db.register_user(user_id)

  @commands.command()
  async def zaps(self, ctx):
    print(f"zaps {ctx.message.author.name}")
    zaps = db.zaps(ctx.message.author.id)
    await ctx.message.channel.send(f"{ctx.message.author.name}: {str(zaps)}")

  @commands.command()
  async def zapleaders(self, ctx):
    zaps = db.zap_leaders()
    print(zaps)
    message = '\n'.join(map(str, zaps))

    await ctx.message.channel.send(f"{message}")