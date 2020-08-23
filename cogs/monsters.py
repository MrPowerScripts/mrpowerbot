import random
import discord
import time
from utils import TEST_CHANNEL, MED_CHANNEL, prob
from discord.ext import commands, tasks

class Monster:
  def __init__(self):
    self.hp = random.randint(10, 20) + 1
    self.escape_time = int(time.time()) + 600
    self.monster_says = "Rawr i'm a monster 〴⋋_⋌〵"

  def is_ded(self):
    return self.hp < 1

  def remove_hp(self, amount):
    self.hp = self.hp - amount

class TestMonster(Monster):
  def __init__(self):
    super().__init__()
    self.hp = random.randint(1, 3)

monster_mash = [Monster, TestMonster]

class Monsters(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.run_monsters.start()
    self.monster = None
    self.monster_message = None

  @commands.Cog.listener()
  async def on_ready(self):
    print("monsters ready")

  @commands.Cog.listener()
  async def on_raw_reaction_add(self, payload):
    if payload.message_id == self.monster_message.id:
      if str(payload.emoji) == "⚡":
        if not self.monster.is_ded():
          self.monster.remove_hp(1)
        else:
          self.monster_message.send(f"monster is ded")

  @tasks.loop(seconds=1.0)
  async def run_monsters(self):
    game_channel = self.bot.get_channel(MED_CHANNEL)
    print('Monster game ready!')
    if prob(.05):
      print("starting monster game")
      # await game_channel.send("starting game")
      self.monster = random.choice(monster_mash)()
      self.monster_message = await game_channel.send(f"{self.monster.monster_says}| hp: {self.monster.hp}")
      await self.monster_message.add_reaction("⚡")
      
      while True:
        if int(time.time()) > self.monster.escape_time:
          await self.monster_message.edit(content=f"{self.monster.monster_says}| hp: ESCAPED")
          break
        if not self.monster.is_ded():
          await self.monster_message.edit(content=f"{self.monster.monster_says}| hp: {self.monster.hp}")
        else:
          await self.monster_message.edit(content=f"{self.monster.monster_says}| hp: ded")
          break
        time.sleep(1)
    time.sleep(10)

def setup(bot):
  bot.add_cog(Monsters(bot))