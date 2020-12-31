from discord.ext import commands, tasks
from utils import (
  ANNOUNCE_CHANNEL,
  MRPOWER_ROLE,
)

class Reddit(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  @commands.has_role(MRPOWER_ROLE)
  async def postr(self, ctx, title: str, content: str):
    print(f"title is: {title}")
    print(f"content is: {content}")

def setup(bot):
  bot.add_cog(Reddit(bot))