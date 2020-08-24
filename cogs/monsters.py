import random
import discord
import time
from utils import TEST_CHANNEL, MRPSBOT_CHANNEL, MONSTERS_ROLE, prob
from discord.ext import commands, tasks

class Monster:
  def __init__(self):
    self.hp = random.randint(10, 20) + 1
    self.name = "Monster"
    self.image = "〴⋋_⋌〵"
    self.status = "Rawr"
    self.escape_time = int(time.time()) + 600

  def is_ded(self):
    return self.hp < 1

  def remove_hp(self, amount):
    self.hp = self.hp - amount

class MiniMonster(Monster):
  def __init__(self):
    super().__init__()
    self.name = "Mini Monster"
    self.image = "〴⋋⋌〵"
    self.hp = random.randint(1, 3)

monster_mash = [Monster, MiniMonster]

class Monsters(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.run_monsters.start()
    self.monster = None
    self.monster_meta = None
    self.monster_message = None

  def mm_formated(self):
    return f"""
      <@&{MONSTERS_ROLE}> has arrived!
      {self.monster.image}
      Name: {self.monster.name}
      HP: {self.monster.hp}
      Status: {self.monster.status}
      """[1:-1]

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
    game_channel = self.bot.get_channel(MRPSBOT_CHANNEL)
    print('Monster game ready!')
    if prob(0.009):
      print("starting monster game")
      # await game_channel.send("starting game")
      self.monster = random.choice(monster_mash)()
      self.monster_message = await game_channel.send(mm_formated())
      await self.monster_message.add_reaction("⚡")
      
      while True:
        if int(time.time()) > self.monster.escape_time:
          self.monster.status = "Escaped"
          await self.monster_message.edit(content=mm_formated())
          break
        if not self.monster.is_ded():
          await self.monster_message.edit(content=mm_formated())
        else:
          self.monster.status = "ded"
          await self.monster_message.edit(content=mm_formated())
          break

def setup(bot):
  bot.add_cog(Monsters(bot))