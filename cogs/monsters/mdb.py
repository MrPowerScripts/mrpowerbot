import json
import os
import psycopg2
from utils import MRPOWERBOT
from .utils import config

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

class MonDB():
  def __init__(self, conn=conn):
    self.discord_id = None
    self.conn = conn
    self.cur = self.conn.cursor()
    self.mondata = None
    self.config = None

  def _save(self):
    try:
      self.cur.execute("""
      INSERT INTO users ("mondata", "discord_id") 
      VALUES (%(mondata)s, '%(discord_id)s')
      ON CONFLICT (discord_id) DO UPDATE
      SET mondata = %(mondata)s;
      """, {"discord_id": self.discord_id, "mondata": json.dumps(self.mondata)})
      self.conn.commit()
    except Exception as e:
      print(e)
      raise e

  def _load(self):
    try:
      self.cur.execute("""
      SELECT mondata
      FROM users 
      WHERE discord_id = %(discord_id)s;
      """, {"discord_id": int(self.discord_id)})
      self.mondata = self.cur.fetchone()[0]
      print(f"User MonData: {self.mondata}")
    except Exception as e:
      print(e)
      raise e

  def _save_config(self):
    print("saving config")
    try:
      self.cur.execute("""
      INSERT INTO users ("mondata", "discord_id") 
      VALUES (%(mondata)s, '%(discord_id)s')
      ON CONFLICT (discord_id) DO UPDATE
      SET mondata = %(mondata)s;
      """, {"discord_id": MRPOWERBOT, "mondata": json.dumps(self.config)})
      self.conn.commit()
    except Exception as e:
      print(e)
      raise e

  def _load_config(self):
    try:
      self.cur.execute("""
      SELECT mondata
      FROM users 
      WHERE discord_id = %(discord_id)s;
      """, {"discord_id": int(MRPOWERBOT)})
      self.config = self.cur.fetchone()[0]
      print(f"Bot Config: {self.config}")
    except Exception as e:
      print(e)
      raise e

  #only run this on instance
  def fetch_config(self):
    try:
      self.cur.execute("""
      SELECT mondata
      FROM users 
      WHERE discord_id = %(discord_id)s;
      """, {"discord_id": int(MRPOWERBOT)})
      result = self.cur.fetchone()[0]
      print(f"db result: {result}")
      print(type(result))
      print(f"does this work: {result == '{}'}")
      if not result:
        print("db config empty - using default")
        return config
      else:
        print("loaded config from db")
        return result[0]
      # print(f"Bot Config: {self.config}")
    except Exception as e:
      print(e)
      raise e

  def update_config(self, config, value, load=False):
    if load:
      self._load_config()
    if not config in self.config:
      self.config[config] = 0
    self.config[config] += value
    self._save_config()

  def get_config(self):
    self._load_config()
    return self.config
  
  def save_config(self, config=None):
    print("called save config")
    if config:
      self.config = config
    self._save_config()

  def add_stat(self, stat, value=1):
    self._load()
    if not stat in self.mondata:
      self.mondata[stat] = 0
    self.mondata[stat] += value
    self._save()

def get_stats():
  cursor = conn.cursor()
  try:
    stats = {}
    for stat in ["attacks", 'killing_blows', 'battles', 'solo_kill']:
      cursor.execute(f"""
      SELECT username, mondata->>'{stat}' AS {stat} 
      FROM users 
      WHERE users.mondata != '{{}}'
      AND users.mondata->'{stat}' IS NOT NULL
      ORDER BY (users.mondata->>'{stat}')::INTEGER DESC LIMIT 5; 
      """)
      stats[stat] = cursor.fetchall()
    return stats
  except Exception as e:
    print(e)
    raise e
  finally:
    cursor.close()
