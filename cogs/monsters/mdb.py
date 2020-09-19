import json
import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

class MonDB():
  def __init__(self, conn=conn):
    self.discord_id = ""
    self.conn = conn
    self.cur = self.conn.cursor()
    self.mondata = ""

  class dbcycle():
    def __call__(self, decorated):
      self.__load()
      decorated(self)
      self._save()

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

  @dbcycle
  def add_stat(self, stat, value=1):
    if not stat in self.mondata:
      self.mondata[stat] = 0
    self.mondata[stat] += value

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
