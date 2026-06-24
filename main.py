import os
import db_manager
from atproto import Client
                     
def job():
    # from github secrets
    username = os.environ.get("BLUESKY_USERNAME")
    password = os.environ.get("BLUESKY_PASSWORD")

    if not username or not password:
        print("Error: username and/or password not found in environment secrets.")
        return
    
    #log in
    client = Client()
    client.login(username, password)

    quote = db_manager.get_random_quote()
    if quote:
        client.send_post(text=quote)
        print("Successfully posted to Bluesky!")
    else:
        print("No quote found")

if __name__ == "__main__":
    job()