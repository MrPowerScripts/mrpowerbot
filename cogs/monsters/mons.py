import random
import time

class Monster:
  def __init__(self):
    self.hp = random.randint(10, 20) + 1
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
    self.hp = random.randint(2, 5)

class BattleTwins(Monster):
  def __init__(self):
    super().__init__()
    self.name = "Battle Twins"
    self.image = "つ ◕_◕ ༽つ つ ◕_◕ ༽つ"
    self.hp = random.randint(25, 45)

class PureAnger(Monster):
  def __init__(self):
    super().__init__()
    self.name = "Pure Anger"
    self.image = "ლ(ಠ益ಠ)ლ"
    self.hp = random.randint(40, 60)

class Bear(Monster):
  def __init__(self):
    super().__init__()
    self.name = "Bear"
    self.image = "ʕ•ᴥ•ʔ"
    self.hp = random.randint(5, 15)

class Bully(Monster):
  def __init__(self):
    super().__init__()
    self.name = "Bully"
    self.image = "(ง'̀-'́)ง"
    self.hp = random.randint(5, 40)

class Squid(Monster):
  def __init__(self):
    super().__init__()
    self.name = "Squid"
    self.image = "くコ:彡"
    self.hp = random.randint(4, 28)

class Killer_Turtle(Monster):
  def __init__(self):
    super().__init__()
    self.name = "Killer Turtle"
    self.image = "𓆉"
    self.hp = random.randint(25, 80)
