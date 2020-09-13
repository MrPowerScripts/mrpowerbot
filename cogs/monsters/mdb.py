import json
import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

def save(discord_id, mondata):
  cursor = conn.cursor()
  try:
    cursor.execute("""
    INSERT INTO users ("mondata", "discord_id") 
    VALUES (%(mondata)s, '%(discord_id)s')
    ON CONFLICT (discord_id) DO UPDATE
    SET mondata = %(mondata)s;
    """, {"discord_id": discord_id, "mondata": json.dumps(mondata)})
    conn.commit()
  except Exception as e:
    print(e)
    raise e
  finally:
    cursor.close()

def load(discord_id):
  cursor = conn.cursor()
  try:
    cursor.execute("""
    SELECT mondata
    FROM users 
    WHERE discord_id = %(discord_id)s;
    """, {"discord_id": int(discord_id)})
    mondata = cursor.fetchone()
    print(f"User MonData: {mondata}")
    return mondata[0]
  except Exception as e:
    print(e)
    raise e
  finally:
    cursor.close()

def get_stats():
  cursor = conn.cursor()
  try:
    stats = {}
    for stat in ["attacks", 'killing_blows', 'battles', 'solo_kills']:
      cursor.execute(f"""
      SELECT username, mondata->>'{stat}' AS {stat} 
      FROM users 
      WHERE users.mondata != '{{}}' 
      ORDER BY mondata->>'{stat}' DESC LIMIT 5; 
      """)
      stats[stat] = cursor.fetchall()
    print(stats)
    return stats
  except Exception as e:
    print(e)
    raise e
  finally:
    cursor.close()

