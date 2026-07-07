import sqlite3
from random import randint

class DatabaseManager:
    def __init__(self, db_path="database.db"):
        #encapsulation: db path stored inside the object
        self.db_path = db_path

    def create_table(self):   
        query = """
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_text VARCHAR(255) NOT NULL
        );
        """

        try:
            with sqlite3.connect(self.db_path) as con:
                cur = con.cursor()
                cur.execute(query)
                result = cur.fetchone()
                con.commit()
            return True
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False

    def insert_data(self, post_text):
        query = """
        INSERT INTO posts (post_text) VALUES (?);
        """

        try:
            with sqlite3.connect(self.db_path) as con:
                cur = con.cursor()
                cur.execute(query, (post_text,))
                result = cur.fetchone()
                con.commit()
            return True
        
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
        
    def get_random_post(self):
        query = "SELECT post_text FROM posts ORDER BY RANDOM() LIMIT 1;"

        try:
            with sqlite3.connect(self.db_path) as con:
                cur = con.cursor()
                cur.execute(query)
                result = cur.fetchone()

                if result:
                    return result[0]
                return "No posts found in database"
    
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None

# create_table()
# insert_data()
