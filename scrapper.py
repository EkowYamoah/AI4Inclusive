import requests
import mysql.connector
import re
from datetime import datetime
import time

# --- Twitter API Setup ---
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAMam0AEAAAAAHbEAiRodJGQoGBnF4I03eYuryOQ%3DmPWirTJgurP5gsZJ4twHEIknyH9GVuThoiGV1DmOLPQkqvHeEF"
# BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAMUn0wEAAAAAAPgR3h5oYtI6IyMUo%2FgsJLpb82E%3DXMsAi7RoQBAjps2bgrHp8lAfMJesDgHBW9qCw5EMHDDXY5RDR5"

def create_headers(token):
    return {"Authorization": f"Bearer {token}"}

def search_tweets(query, max_results=10):
    url = "https://api.twitter.com/2/tweets/search/recent"
    headers = create_headers(BEARER_TOKEN)
    params = {
        "query": query,
        "tweet.fields": "tweet_created_at,lang,public_metrics,author_id",
        "expansions": "author_id",
        "user.fields": "created_at,verified,location,public_metrics,name,username",
        "max_results": max_results
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

# --- Preprocessing ---
def preprocess(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"@\w+|#\w+", "", text)
    text = re.sub(r"[^\w\s]", "", text)
    return text.strip()

# --- MySQL DB Connection ---
conn = mysql.connector.connect(
    host='localhost',
    user='yme',
    password='Password@123',
    database='TWEET_DATA_TEST'
)
cursor = conn.cursor()

# --- Query and store ---
query = "mental health Ghana"
data = search_tweets(query, max_results=10)

tweets = data.get('data', [])
users_map = {u['id']: u for u in data.get('includes', {}).get('users', [])}

for tweet in tweets:
    user = users_map.get(tweet['author_id'])
    if not user:
        continue

    tweet_id = int(tweet['id'])
    user_id = int(user['id'])

    # --- Insert User ---
    cursor.execute("""
        INSERT IGNORE INTO users (id, username, display_name, verified, followers_count, following_count, location, account_created_at, inserted_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())
    """, (
        user_id,
        user['username'],
        user['name'],
        user.get('verified', False),
        user['public_metrics'].get('followers_count', 0),
        user['public_metrics'].get('following_count', 0),
        user.get('location'),
        user.get('created_at')
    ))

    # --- Insert Raw Tweet ---
    cursor.execute("""
        INSERT IGNORE INTO raw_tweets (
            id, user_id, content, tweet_created_at, language, 
            retweet_count, like_count, quote_count, reply_count, 
            is_retweet, url, inserted_at
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
    """, (
        tweet_id,
        user_id,
        tweet['text'],
        tweet['created_at'],
        tweet['lang'],
        tweet['public_metrics'].get('retweet_count', 0),
        tweet['public_metrics'].get('like_count', 0),
        tweet['public_metrics'].get('quote_count', 0),
        tweet['public_metrics'].get('reply_count', 0),
        False,  # We can't confirm retweet from API here
        f"https://twitter.com/{user['username']}/status/{tweet_id}"
    ))

    # --- Preprocessed Tweet ---
    processed_text = preprocess(tweet['text'])
    cursor.execute("""
        INSERT IGNORE INTO processed_tweets (tweet_id, preprocessed_text, model_version, preprocessing_pipeline, inserted_at)
        VALUES (%s, %s, %s, %s, NOW())
    """, (
        tweet_id,
        processed_text,
        'v1.0',
        'lowercase, remove_links, remove_mentions_hashtags, remove_punctuation'
    ))

    time.sleep(1)  # Respect Twitter API rate limits

conn.commit()
cursor.close()
conn.close()
print("Done inserting tweets.")
