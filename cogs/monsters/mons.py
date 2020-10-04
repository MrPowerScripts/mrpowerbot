import random
import time

monster_meta = [
  {"name": "Mini Monster", "image": "〴⋋⋌〵"},
  {"name": "Battle Twins", "image": "つ ◕_◕ ༽つ つ ◕_◕ ༽つ"},
  {"name": "Pure Anger", "image": "ლ(ಠ益ಠ)ლ"},
  {"name": "Bear", "image": "ʕ•ᴥ•ʔ"},
  {"name": "Bully", "image": "(ง'̀-'́)ง"},
  {"name": "Squid", "image": "くコ:彡"},
  {"name": "Killer Turtle", "image": "𓆉"},
]

class Monster():
  def __init__(self, level=1, blueprint=None):
    if not blueprint:
      blueprint = random.choice(monster_meta)
    self.hp = (random.randint(1, 2) + 1) * level
    self.max_hp = 0
    self.name = blueprint['name']
    self.image = blueprint['image']
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
