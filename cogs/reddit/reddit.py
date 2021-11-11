import discord
from discord.ext import commands, tasks
import praw
import os
import validators
from utils import (
  ANNOUNCE_CHANNEL,
  MRPOWER_ROLE,
  REDDIT_NOTIFY_ROLE
)

reddit = praw.Reddit(client_id=os.environ['REDDIT_CLIENT_ID'],
                     client_secret=os.environ['REDDIT_CLIENT_SECRET'],
                     password=os.environ['REDDIT_PASSWORD'],
                     user_agent="mrpowerbot script by u/mrpowerscripts",
                     username="mrpowerbot")

class Reddit(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.rapi = reddit
    self.mrpssub = self.rapi.subreddit("mrpowerscripts")
    self.announce_channel = discord.utils.get(self.bot.get_all_channels(), id=ANNOUNCE_CHANNEL)

  @commands.Cog.listener()
  async def on_ready(self):
    print(f"reddit account: {self.rapi.user.me()}")

  @commands.command()
  @commands.has_role(MRPOWER_ROLE)
  async def postr(self, ctx, title: str, content: str):
    
    print(f"title is: {title}")
    print(f"content is: {content}")
    
    if validators.url(content.strip()):
      params = {"title": title, "url": content.strip()}
    else:
      params = {"title": title, "selftext": content}
    
    try:
      post = self.mrpssub.submit(**params)
      
      announce_channel = discord.utils.get(self.bot.get_all_channels(), id=ANNOUNCE_CHANNEL)
      await announce_channel.send(f"New <@&{REDDIT_NOTIFY_ROLE}> post!\n https://reddit.com/{post.permalink}")
    except Exception as e:
      print(e)


def setup(bot):
  bot.add_cog(Reddit(bot))