from ...db import conn
import json

def save(mondata):
  cursor = conn.cursor()
  try:
    cursor.execute("""
    INSERT INTO users ("mondata") 
    VALUES ('%(mondata)s')
    """, {"mondata": json.dumps(mondata)})
    conn.commit()
  except Exception as e:
    print(e)
    raise e
  finally:
    cursor.close()

def load(mondata):
  cursor = conn.cursor()
  try:
    cursor.execute("""
    SELECT * FROM users ("mondata") 
    """)
  
  except Exception as e:
    print(e)
    raise e
  finally:
    cursor.close()