import random
import discord
import time
from utils import TEST_CHANNEL, MRPSBOT_CHANNEL, MONSTERS_ROLE, MOD_ROLE, prob
from discord.ext import commands, tasks
from collections import Counter

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
    if self.hp < 1:
      self.status = 'ded'

  def times_up(self):
    if int(time.time()) > self.escape_time:
      self.status = "escaped"
      return True
    else:
      return False

  def battle_over(self):
    return self.times_up() or self.is_ded()

class MiniMonster(Monster):
  def __init__(self):
    super().__init__()
    self.name = "Mini Monster"
    self.image = "〴⋋⋌〵"
    self.hp = random.randint(2, 5)

monster_mash = [Monster, MiniMonster]

class Monsters(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.probability = 0.0009
    self.run_monsters.start()
    self.monster = None
    self.monster_meta = {
      attackers:[]
      }
    self.monster_message = None

  @commands.command()
  @commands.has_role(MOD_ROLE)
  async def monprob(self, ctx, arg):
    if float(arg):
      self.probability = float(arg)
      print(f"new probability: {self.probability}")

  def mm_formated(self):
    return f"""
      <@&{MONSTERS_ROLE}> has arrived!
      {self.monster.image}
      `Name:` {self.monster.name}
      `HP:` {self.monster.hp}
      `Status:` {self.monster.status}
      {f"Attackers: {Counter(self.monster_meta.attackers)}" if self.monster.battle_over() else ""}
      """[1:-1]

  @commands.Cog.listener()
  async def on_ready(self):
    print("monsters ready")

  @commands.Cog.listener()
  async def on_raw_reaction_add(self, payload):
    if payload.message_id == self.monster_message.id:
      if str(payload.emoji) == "⚡":
        if not self.monster.is_ded():
          self.monster_meta.attackers.append(payload.member.name)
          self.monster.remove_hp(1)
        else:
          self.monster_message.send(f"monster is ded")

  @tasks.loop(seconds=1.0)
  async def run_monsters(self):
    game_channel = self.bot.get_channel(MRPSBOT_CHANNEL)
    print('Monster game ready!')
    if prob(self.probability):
      print("starting monster game")
      # await game_channel.send("starting game")
      self.monster = random.choice(monster_mash)()
      print(self.mm_formated())
      self.monster_message = await game_channel.send(self.mm_formated())
      await self.monster_message.add_reaction("⚡")
      
      while True:
        if self.monster.times_up():
          await self.monster_message.edit(content=self.mm_formated())
          break
        if not self.monster.is_ded():
          await self.monster_message.edit(content=self.mm_formated())
        else:
          await self.monster_message.edit(content=self.mm_formated())
          break

def setup(bot):
  bot.add_cog(Monsters(bot))