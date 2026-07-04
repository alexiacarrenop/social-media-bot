import queue
import threading
import time
import os
from abc import ABC, abstractmethod
from db_manager import DatabaseManager
from atproto import Client

lyric_queue = queue.Queue()
db_lock = threading.Lock()


#1. Abstraction: the template
class SocialMediaPlatform(ABC):
    @abstractmethod
    def login(self):
        """Every platform must know its won process of authentication"""
        pass

    @abstractmethod
    def post(self, content):
        """Every platform must know how to post content"""
        pass

#2. inheritance and polymorphism: bluesky 
class BlueskyPlatform(SocialMediaPlatform):
    def __init__(self):
        # encapsulation: double underscores hide credential inside the class. from github secrets
        self.__username = os.environ.get("BLUESKY_USERNAME")
        self.__password = os.environ.get("BLUESKY_PASSWORD")
        self.client = Client()
    
    def login(self):
        if not self.__username or not self.__password:
            print("Error: Bluesky credentials missing from environment.")
            return False
        try:
            self.client.login(self.__username, self.__password)
            print("Logged into Bluesky successfully.")
            return True
        except Exception as e:
            print(f"Bluesky login failed: {e}")
            return False
        
    def post(self, content):
        try:
            self.client.send_post(text=content)
            print("Posted to Bluesky successfully.")
            return True
        except Exception as e:
            print(f"Failed to post to Bluesky: {e}")
            return False

def producer_job(db_path):
    """Fetches from database and sends to queue"""
    db = DatabaseManager(db_path)

    #use lock to read safely from db
    with db_lock:
        text_to_post = db.get_random_post()

    if text_to_post and text_to_post != "No posts found in database":
        print(f"[Producer] Found lyric and adding to queue: {text_to_post}")
        lyric_queue.put(text_to_post)
    else:
        print(f"[Producer] No posts found in database.") 
        lyric_queue.put(None)

def consumer_job():
    """Fetches from queue and posts it"""
    text_to_post = lyric_queue.get()

    if text_to_post is None:
        print(f"[Consumer] Received empty signal. Exiting...")
        lyric_queue.task_done()
        return

    print(f"[Consumer] Fetched lyric from queue. Starting upload..") 
    bot : SocialMediaPlatform = BlueskyPlatform()
    if bot.login(): 
        bot.post(text_to_post)

    lyric_queue.task_done()
    
#3. refactor
def main():
    db_path = "database.db"

    #create two threads
    producer_thread = threading.Thread(target=producer_job, args=(db_path,))
    consumer_thread = threading.Thread(target=consumer_job)

    #start both threads
    producer_thread.start()
    consumer_thread.start()

    #wait for both threads to finish running before closing app
    producer_thread.join()
    consumer_thread.join()
    print("Main: both threads executed successfully")

if __name__ == "__main__":
    main()