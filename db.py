import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

def preparedb():
  cursor = conn.cursor()
  try:
    cursor.execute("""
      CREATE TABLE IF NOT EXISTS users
      (
        id serial,
        discord_id integer,
        zaps integer
      );
    """)
    conn.commit()
  except Exception as e:
    print(e)
    raise e
  finally:
    cursor.close()


def status_check():
  cursor = conn.cursor()
  try:
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    cursor.close()
    return version
  
  except Exception as e:
    print(e)
    raise e
  finally:
    cursor.close()

