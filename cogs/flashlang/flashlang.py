import random
import discord
import time
import csv
from pathlib import Path
from bot import client

from utils import (
  TEST_CHANNEL, MRPSBOT_CHANNEL,
  MOD_ROLE, MRPOWERBOT,  prob
  )
from discord.ext import commands, tasks
from collections import Counter

p = Path(__file__)
this_dir = p.parent.absolute()

class Flashlang(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.translations = None
    self.ready = False
    self.run_flashlang.start()

  @commands.Cog.listener()
  async def on_ready(self):
    self.game_channel = self.bot.get_channel(MRPSBOT_CHANNEL)
    self.load_language()
    self.ready = True
    print("flashlang ready")


  @tasks.loop(seconds=20.0)
  async def run_flashlang(self):
    print("running flashlang")
    if self.ready:
      print("flashlang ran")
      word = random.choice(self.translations)
      message = await self.game_channel.send(f"{word[0]} is {word[1]}")


  def load_language(self, lang='de'):
    # Read CSV file
    with open(f"{this_dir}/translations-{lang}.csv") as fp:
        reader = csv.reader(fp, delimiter=",", quotechar='"')
        # next(reader, None)  # skip the headers
        data_read = [row for row in reader]
        self.translations = data_read

    def run():
      pass


def setup(bot):
  bot.add_cog(Flashlang(bot))