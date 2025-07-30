import snscrape.modules.twitter as sntwitter
import mysql.connector
from datetime import datetime
import re

# --- Connect to MySQL database ---
conn = mysql.connector.connect(
    host='localhost',
    user='yme',
    password='Password@123',
    database='TWEET_DATA_TEST'
)
cursor = conn.cursor()

# --- Basic tweet preprocessing ---
def preprocess(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"@\w+|#\w+", "", text)
    text = re.sub(r"[^\w\s]", "", text)
    return text.strip()

# --- Scrape tweets using snscrape ---
query = "mental health Ghana since:2024-01-01 until:2025-01-01"
limit = 20
now = datetime.utcnow()  # capture the timestamp of data ingestion

for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
    if i >= limit:
        break

    user = tweet.user
    tweet_id = tweet.id
    user_id = user.id

    # --- Insert user ---
    cursor.execute("""
        INSERT IGNORE INTO users (
            id, username, display_name, verified, followers_count,
            following_count, location, created_at, created_date
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        user_id, user.username, user.displayname, user.verified,
        user.followersCount, user.friendsCount, user.location,
        user.created, now
    ))

    # --- Insert raw tweet ---
    cursor.execute("""
        INSERT IGNORE INTO raw_tweets (
            id, user_id, content, created_at, language,
            retweet_count, like_count, quote_count, reply_count,
            is_retweet, url, created_date, tweet_date
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        tweet_id, user_id, tweet.content, tweet.date, tweet.lang,
        tweet.retweetCount, tweet.likeCount, tweet.quoteCount,
        tweet.replyCount, tweet.retweetedTweet is not None,
        tweet.url, now, tweet.date
    ))
    
    # --- Insert preprocessed tweet ---
    processed_text = preprocess(tweet.content)
    cursor.execute("""
        INSERT IGNORE INTO processed_tweets (
            tweet_id, preprocessed_text, model_version,
            preprocessing_pipeline, processed_at, created_date
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        tweet_id, processed_text, 'v1.0',
        'lowercase, remove_links, remove_mentions_hashtags, remove_punctuation',
        now, now
    ))

# --- Commit all inserts ---
conn.commit()
cursor.close()
conn.close()
