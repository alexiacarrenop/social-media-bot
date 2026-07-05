# Universal Social Media Bot

A smart, free, and automated tool that grabs posts from a database and posts them to any social media platform. 

It runs completely in the cloud using **GitHub Actions**, meaning you don't need a server and it's free to run.

---

## How It Works

Instead of just running a simple script, this bot is flexible and safe:

* **Adaptable to any platforms:** The code is built using a universal template. Right now, it's set up for Bluesky, but you can swap or add platforms (like X) by simply writing a new connector. The rest of the bot stays exactly the same.
* **Multi-threading:** To keep things fast, the bot splits its work into two background workers that run at the same time. One worker safely grabs a post from your database, and the other worker connects to the internet to publish it. 
* **Database protection:** Because multiple things are happening at once, the bot uses a virtual "lock" to make sure your database never gets mixed up or corrupted.

---

## Class Diagram

This diagram shows how the different files and templates talk to each other inside the code:

```mermaid
classDiagram
    direction LR
    
    class SocialMediaPlatform {
        <<abstract template>>
        +login()
        +post(content)
    }
    
    class BlueskyPlatform {
        +login()
        +post(content)
    }
    
    class DatabaseManager {
        +get_random_post()
    }
    
    class MainEngine {
        +producer_job()
        +consumer_job()
        +main()
    }

    SocialMediaPlatform <|-- BlueskyPlatform : Plugs into the template
    MainEngine --> DatabaseManager : Safe database fetch
    MainEngine --> SocialMediaPlatform : Passes post to the platform