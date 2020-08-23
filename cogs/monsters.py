import random
import discord
import time
from utils import TEST_CHANNEL
from discord.ext import commands

class Monster:
  def __init__(self):
    self.hp = random.randint(10, 20)

  def remove_hp(self, amount):
    self.hp = self.hp - amount

class TestMonster(Monster):
  def __init__(self):
    self.hp = randomm.randint(1, 3)

monster_mash = [Monster, TestMonster]

class Monsters(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    game_channel = self.bot.get_channel(TEST_CHANNEL)
    test_message = await game_channel.send("monster game initialized")
    print('Monster game ready!')
    
    while True:
      time.sleep(5)
      game_channel.send("starting game")
      monster = random.choice(monster_mash)()
      game_channel.send(f"monster hp is: {monster.hp}")
      monster.remove_hp(5)
      game_channel.send(f"monster hp is: {monster.hp}")
      
      time = random.randint(1, 3600)
      game_channel.send(f"new gammme in: {time}")
      time.sleep(time)

  # @commands.Cog.listener()
  # async def on_message(self, message):
  #   print(message)

def setup(bot):
  bot.add_cog(Monsters(bot))