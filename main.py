import os
from abc import ABC, abstractmethod
from db_manager import DatabaseManager
from atproto import Client

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
    
#3. refactor
def main():
    # initialise database 
    db = DatabaseManager("database.db")
    text_to_post = db.get_random_post()

    if text_to_post and text_to_post != "No posts found in database":
        
        bot : SocialMediaPlatform = BlueskyPlatform()

        if bot.login():
            bot.post(text_to_post)
    else:
        print("No quote found")

if __name__ == "__main__":
    main()