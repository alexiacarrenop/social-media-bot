import unittest
import sqlite3
import threading
import os 
from db_manager import DatabaseManager
from main import producer_job, lyric_queue, BlueskyPlatform

class TestBot(unittest.TestCase):
    def setUp(self):
        #run before every test case
        self.db_path = ":memory:"
        self.db = DatabaseManager(self.db_path)
        self.db.create_table()
    
    def tearDown(self):
        #run after every test case
        if hasattr(self.db, 'con') and self.db.con:
            self.db.con.close()
    
        del self.db
        print("[Clean up] Temporary in-memory database deleted successfully")

    def test_create_table(self):
        with sqlite3.connect(self.db_path) as con:
            cur = con.cursor()
            cur.execute("PRAGMA table_info(posts);")
            result = cur.fetchall()

        self.assertEqual(len(result), 2, "Table should have exactly 2 columns")

        self.assertEqual(result[0][1], "id", "First column should be 'id")
        self.assertEqual(result[1][1], "post_text", "Second column should be 'post_text")

    def test_fetching_from_empty(self): #fetching from empty database
        result = self.db.get_random_post()

        self.assertEqual(result, "No posts found in database")

    def test_fetching_with_data(self):
        with sqlite3.connect(self.db_path) as con:
            cur = con.cursor()
            cur.execute("INSERT INTO posts (post_text) VALUES ('Hello Bluesky');")
            con.commit()

        result = self.db.get_random_post()
        
        self.assertEqual(result, "Hello Bluesky")

    def test_producer(self):
        with sqlite3.connect(self.db_path) as con:
            cur = con.cursor()
            cur.execute("INSERT INTO posts (post_text) VALUES ('Hello Bluesky);")
            con.commit()

        while not lyric_queue.empty():
            lyric_queue.get()

        producer_thread = threading.Thread(target=producer_job, args=(self.db))
        producer_thread.start()
        producer_thread.join()

        self.assertFalse(lyric_queue.empty(), "Queue should not be empty")

        queue_result = lyric_queue.get()
        self.assertEqual(queue_result, "Hello Bluesky")

    def test_empty_db_producer(self):
        while not lyric_queue.empty():
            lyric_queue.get()

        producer_thread = threading.Thread(target=producer_job, args=(self.db))
        producer_thread.start()
        producer_thread.join()

        self.assertEqual(self.db.get_random_post(), "No posts found in database")
        self.assertIsNone(lyric_queue.get())

    def test_missing_credentials(self):
        old_username = os.environ.get("BLUESKY_USERNAME")
        old_password = os.environ.get("BLUESKY_PASSWORD")

        os.environ.pop("BLUESKY_USERNAME", None)
        os.environ.pop("BLUESKY_PASSWORD", None)

        try:
            bot = BlueskyPlatform()

            login_result = bot.login()
            self.assertFalse(login_result, "Login should return False when credentials are missing")
        
        finally:
            if old_username is not None:
                    os.environ["BLUESKY_USERNAME"] = old_username
            if old_password is not None:
                    os.environ["BLUESKY_PASSWORD"] = old_password

        

if __name__ == "__main__":
    unittest.main()