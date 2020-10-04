import random
import time

class Monster(level=):
  def __init__(self, level=1):
    self.hp = (random.randint(1, 2) + 1) * level
    self.max_hp = 0
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

class BattleTwins(Monster):
  def __init__(self, level=1):
    super().__init__()
    self.name = "Battle Twins"
    self.image = "つ ◕_◕ ༽つ つ ◕_◕ ༽つ"

class PureAnger(Monster):
  def __init__(self, level=1):
    super().__init__()
    self.name = "Pure Anger"
    self.image = "ლ(ಠ益ಠ)ლ"

class Bear(Monster):
  def __init__(self, level=1):
    super().__init__()
    self.name = "Bear"
    self.image = "ʕ•ᴥ•ʔ"

class Bully(Monster):
  def __init__(self, level=1):
    super().__init__()
    self.name = "Bully"
    self.image = "(ง'̀-'́)ง"

class Squid(Monster):
  def __init__(self, level=1):
    super().__init__()
    self.name = "Squid"
    self.image = "くコ:彡"

class Killer_Turtle(Monster):
  def __init__(self, level=1):
    super().__init__()
    self.name = "Killer Turtle"
    self.image = "𓆉"
