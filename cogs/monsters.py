import random
import discord
import time
from utils import TEST_CHANNEL, prob
from discord.ext import commands

class Monster:
  def __init__(self):
    self.hp = random.randint(10, 20)

  def is_ded(self):
    return self.hp < 1

  def remove_hp(self, amount):
    self.hp = self.hp - amount

class TestMonster(Monster):
  def __init__(self):
    self.hp = random.randint(1, 3)

monster_mash = [Monster, TestMonster]

class Monsters(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.monster = None
    self.monster_message = None

  @commands.Cog.listener()
  async def on_ready(self):
    game_channel = self.bot.get_channel(TEST_CHANNEL)
    self.monster_message = await game_channel.send("monster game initialized")
    print('Monster game ready!')
    
    time.sleep(5)

    while True:
      if prob(.10):
        await game_channel.send("starting game")
        self.monster = random.choice(monster_mash)()

        self.bot.add_reaction(self.monster_message, "⚡")
        
        while not self.monster.is_ded():
          await self.monster_message.send(f"monster hp is: {self.monster.hp}")
          time.sleep(5)
      time.sleep(1)

  @commands.Cog.listener()
  async def on_raw_reaction_add(oayload):
    if payload.message_id == self.monster_message.id:
      if str(payload.emoji) == "⚡":
        if not self.monster.is_ded():
          self.monster.remove_hp(1)
        else:
          self.monster_message.send(f"monster is ded")

def setup(bot):
  bot.add_cog(Monsters(bot))