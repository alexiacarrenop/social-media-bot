import sqlite3
from random import randint

con = sqlite3.connect("database.db")
cur = con.cursor()

def create_table():   
    cur.execute("CREATE TABLE posts(" \
    "id INTEGER PRIMARY KEY AUTOINCREMENT, " \
    "post_text VARCHAR(255) NOT NULL, " \
    "scheduled_date TEXT," \
    "has_been_posted BOOLEAN DEFAULT 0)")
    con.commit()

def insert_data():
    cur.execute("""
    INSERT INTO posts (post_text, scheduled_date)
VALUES
  ('some flowers bloom when the green grass grows. our praise is not for them, but the ones who bloom in the bitter snow. we raise our cups to them.', '2026-06-23'),
  ('i knew you before we met, and i don’t even know you yet. all i know is you’re someone i have always known.', '2026-06-24'),
  ('i am more than memory. i am what might be, i am mystery. you know me, so show me.', '2026-06-25'),
  ('take it from a woman of my age: there is nothing love can’t change. even when the bricks are stacked, love is blooming through the cracks. even when the light is gone, love is reaching for the sun. it was love that spun the world, when i was a young girl.', '2026-06-26'),
  ('love is patient, love is kind. it always protects, always trusts, always hopes, always perseveres. love never fails.', '2026-06-27'),
  ('melt with you ‘til it all turns black' || CHAR(10) || 'when you get so close and you can’t go back', '2026-06-28');
    """)
    con.commit()

def get_random_quote():
    num = randint(1,3)
    
    cur.execute("SELECT post_text FROM posts WHERE id = (?)", (num,))    
    result = cur.fetchone()

    if result:
        return result[0]
    return None

# create_table()
# insert_data()
