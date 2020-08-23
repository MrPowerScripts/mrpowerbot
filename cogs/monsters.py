import random
import discord
from utils import TEST_CHANNEL
from discord.ext import commands

class Monster:
  def __init__(self):
    self.hp = random.randint(10, 20)


class TestMonster(Monster):
  def __init__(self):
    self.hp = randomm.randint(1, 3)


class Monsters(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    game_channel = self.bot.get_channel(TEST_CHANNEL)
    await game_channel.send("monster game initialized")
    print('Monster game ready!')


  @commands.Cog.listener()
  async def on_message(self, message):
    print(message)

def setup(bot):
  bot.add_cog(Monsters(bot))