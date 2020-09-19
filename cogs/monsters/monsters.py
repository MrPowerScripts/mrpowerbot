import random
import discord
import time
import db
from bot import client
from . import mdb
from .mdb import MonDB
from .mons import (
  Monster,
  MiniMonster,
  BattleTwins,
  Bear,
  PureAnger
)

monster_mash = [Monster, MiniMonster, BattleTwins, Bear, PureAnger]

from utils import (
  TEST_CHANNEL, MRPSBOT_CHANNEL, MONSTERS_ROLE, 
  MOD_ROLE, MRPOWERBOT,  prob
  )
from discord.ext import commands, tasks
from collections import Counter

class Monsters(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.mdb = monDB()
    self.probability = 0.0005
    self.last_run = 0
    self.respawn_limit = 3600
    self.run_monsters.start()
    self.monster = None
    self.battling = False
    self.killing_blow = None
    self.monster_attackers = Counter()
    self.monster_message = None
    self.game_channel = None

  @commands.command()
  @commands.has_role(MOD_ROLE)
  async def monprob(self, ctx, arg):
    if float(arg):
      self.probability = float(arg)
      print(f"new probability: {self.probability}")

  @commands.command()
  async def monstats(self, ctx):
    try:
      print("getting stats")
      stats = self.mdb.get_stats()
      statsfmted  = ""
      for action in stats.keys():
        statsfmted += f'----------{action}------------\n'
        statsfmted += '\n'.join(map(lambda m: f"{m[0]}: {m[1]}", stats[action]))
        #print(statsfmted.join(map(str, stats[action])))
        statsfmted += '\n\n'

        # statsf[action] = list(map(lambda m: f"{stats[action][0][0]}: {stats[action][1]}", stats[action]))
      
      await ctx.channel.send(statsfmted)
      # return f"""
      #   {statsf}
      #   """[1:-1]
    except Exception as e:
      print(e)

  def mm_formated(self):
    print("updaing monster message")
    battle_over = self.battle_over()
    try:
      if battle_over:
        print("battle is over")
        attackers = list(map(lambda m: f"<@{m}>: {self.monster_attackers[m]}", self.monster_attackers))
        print("attackers listed")
      return f"""
        <@&{MONSTERS_ROLE}> has arrived! Tap ⚡ repeatedly to attack!
        {self.monster.image}
        `Name:` {self.monster.name}
        `HP:` {self.monster.hp}/{self.monster.max_hp}
        `Status:` {self.monster.status}
        {f"`Attackers:` {attackers}" if battle_over else ""}
        {f"`Killing Blow:` <@{self.killing_blow}>" if battle_over and self.killing_blow != None else ""}
        """[1:-1]
    except Exception as e:
      print(e)
  
  def battle_over(self):
    if self.monster.times_up() or self.monster.is_ded():
      # print("the battle is over")
      return True
    else:
      return False

  async def start_battle(self):
    # print("starting monster game")
    try:
      self.monster = random.choice(monster_mash)()
      self.monster.max_hp = self.monster.hp
      self.killing_blow = None
    except Exception as e:
      print(e)
    # print("monster created.")
    self.monster_attackers.clear()
    # print("monster attackers cleared")
    message = await self.game_channel.send(self.mm_formated())
    # print('monster messaged created')
    self.monster_message = message
    # print(message)
    await self.monster_message.add_reaction("⚡")
    self.battling = True
    print(self.mm_formated())

  async def end_battle(self):
    # final update before reset
    self.battling = False
    self.last_run = int(time.time())

    # mpbzaps = db.zaps(MRPOWERBOT)

    atckr_count = len(self.monster_attackers.values())
    # solo kills
    if atckr_count== 1:
      attacker = self.monster_attackers.most_common()[0][0]
      self.mondb.discord_id = attacker
      self.mondb.add_stat('solo_kill')
    #Attacks
    for attacker in self.monster_attackers:
      # zaps
      # attacker_user = client.get_user(attacker)
      # db.zap(attacker_user, value=self.monster_attackers[attacker]) 
      self.mondb.discord_id = attacker
      #Battles
      self.mondb.add_stat('battles')
      # Attacks
      self.mondb.add_stat('attacks', self.monster_attackers[attacker])
      #Killing blows
      if attacker == self.killing_blow:
        self.mondb.add_stat('killing_blows')

    #remove mrpowerbot zaps
    # mpb_user = client.get_user(MRPOWERBOT)
    # db.zap(mpb_user, value=mpbzaps, remove=True)
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
            if self.monster.hp < 1 and self.killing_blow == None:
              self.killing_blow = payload.member.id
            self.monster_attackers[payload.member.id] += 1
            print(self.monster_attackers)
            if self.battle_over():
              await self.end_battle()

  @tasks.loop(hours=12)
  async def auto_stats(self, ctx):
    await ctx.invoke(self.bot.get_command('play'), query='hi')

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