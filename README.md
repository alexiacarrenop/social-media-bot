# Bluesky Lyric Bot

A serverless Python bot that automatically selects random lyrics from an SQL database and posts them directly to Bluesky. 

The project runs completely free using **GitHub Actions**.

---

## How It Works

* **Database Integration:** Built using a SQLite database structure to manage a collection of lyrics.
* **Automation Pipeline:** Driven by a GitHub Actions YAML schedule runner that wakes up daily, logs into the platform, and posts the content.
* **Secure Environment:** Uses hidden GitHub Repository Secrets to protect account credentials (username and password).

---

## Project Structure

```text
├── .github/workflows/
│   └── scheduler.yml      # GitHub Actions automation schedule
├── db_manager.py          # Script containing database setup and selector logic
├── main.py                # Main execution loop connecting to Bluesky API
└── README.md              # Documentation
```

## Setting It Up 

To run this  yourself, you must insert your login credentials securely into your repository settings:

1. Navigate to your repository on **GitHub.com** and click the **Settings** gear tab.
2. On the left sidebar, scroll down to expand **Secrets and variables**, then click **Actions**.
3. Click the green **New repository secret** button at the top right.

| Secret Name | Expected Value |
| :--- | :--- |
| **`BLUESKY_USERNAME`** | Your username *(e.g., username.bsky.social)* |
| **`BLUESKY_PASSWORD`** | An App Password generated in your Bluesky settings |

> ⚠️ **Important:** Do not use your main account password. Always generate a unique App Password inside your Bluesky account settings (*Settings -> App Passwords*) to keep your credentials safe.
