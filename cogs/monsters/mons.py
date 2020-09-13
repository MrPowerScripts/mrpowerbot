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