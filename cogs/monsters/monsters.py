import random
import discord
import time
from utils import (
  TEST_CHANNEL, MRPSBOT_CHANNEL, MONSTERS_ROLE, 
  MOD_ROLE, MRPOWERBOT, prob
  )
from discord.ext import commands, tasks
from collections import Counter

class Monster:
  def __init__(self):
    self.hp = random.randint(10, 20) + 1
    self.max_hp = self.hp
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
    self.probability = 0.0001
    self.last_run = 0
    self.respawn_limit = 86400
    self.run_monsters.start()
    self.monster = None
    self.battling = False
    self.monster_attackers = Counter()
    self.monster_message = None
    self.game_channel = None

  @commands.command()
  @commands.has_role(MOD_ROLE)
  async def monprob(self, ctx, arg):
    if float(arg):
      self.probability = float(arg)
      print(f"new probability: {self.probability}")
      
  def wtf(self, wtf):
    return f"<@{wtf}>: {self.monster_attackers[wtf]}"

  def mm_formated(self):

    if self.battle_over():
      attackers = list(map(lambda m: self.wtf(m), self.monster_attackers))
    return f"""
      <@&{MONSTERS_ROLE}> has arrived!
      {self.monster.image}
      `Name:` {self.monster.name}
      `HP:` {self.monster.hp}/{self.max_hp}
      `Status:` {self.monster.status}
      {f"`Attackers:` {attackers}" if self.battle_over() else ""}
      """[1:-1]

  def battle_over(self):
    if self.monster.times_up() or self.monster.is_ded():
      print("the battle is over")
      return True
    else:
      return False

  async def start_battle(self):
    print("starting monster game")
    self.monster = random.choice(monster_mash)()
    self.monster_attackers.clear()
    message =  await self.game_channel.send(self.mm_formated())
    self.monster_message = message
    print(message)
    await self.monster_message.add_reaction("⚡")
    self.battling = True
    print(self.mm_formated())

  async def end_battle(self):
    # final update before reset
    self.battling = False
    self.last_run = int(time.time())
    await self.monster_message.edit(content=self.mm_formated())
  
  @commands.Cog.listener()
  async def on_ready(self):
    self.game_channel = self.bot.get_channel(MRPSBOT_CHANNEL)
    print("monsters ready")

  @commands.Cog.listener()
  async def on_raw_reaction_add(self, payload):
    if self.battling:
      if payload.message_id == self.monster_message.id:
        if str(payload.emoji) == "⚡":
          if payload.user_id != MRPOWERBOT:
            self.monster.remove_hp(1)
            self.monster_attackers[payload.member.id] += 1
            print(self.monster_attackers)
            if self.battle_over():
              self.end_battle()

  @tasks.loop(seconds=1.0)
  async def run_monsters(self):
    if prob(self.probability):
      print("HIT - should we play?")
      if int(time.time()) > (self.last_run + self.respawn_limit):
        await self.start_battle()
      else:
        print(f"Too Soon... last run: {self.last_run}, current: {time.time()}")
      
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