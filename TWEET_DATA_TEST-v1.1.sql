CREATE DATABASE TWEET_DATA_TEST;
USE TWEET_DATA_TEST;

-- 1. Users table (same)
CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY,
    username VARCHAR(255),
    display_name VARCHAR(255),
    verified BOOLEAN,
    followers_count INT,
    following_count INT,
    location VARCHAR(255),
    created_at DATETIME
);

-- 1. Raw Tweets Table
CREATE TABLE IF NOT EXISTS raw_tweets (
    id BIGINT PRIMARY KEY,
    user_id BIGINT,
    content TEXT,
    created_at DATETIME,
    language VARCHAR(10),
    retweet_count INT,
    like_count INT,
    quote_count INT,
    reply_count INT,
    is_retweet BOOLEAN,
    url TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 2. Preprocessed Tweets Table
CREATE TABLE IF NOT EXISTS  processed_tweets (
    tweet_id BIGINT PRIMARY KEY,
    preprocessed_text TEXT,
    model_version VARCHAR(50),      -- Which model processed this tweet
    preprocessing_pipeline TEXT,    -- Optional: e.g., "lowercase, remove_stopwords, lemmatize"
    processed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tweet_id) REFERENCES raw_tweets(id)
);


-- 3. Hashtags table (same)
CREATE TABLE IF NOT EXISTS  hashtags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    text VARCHAR(255) UNIQUE
);

-- 4. Tweet-Hashtag Join Table (same)
CREATE TABLE IF NOT EXISTS  tweet_hashtags (
    tweet_id BIGINT,
    hashtag_id INT,
    PRIMARY KEY (tweet_id, hashtag_id),
    FOREIGN KEY (tweet_id) REFERENCES tweets(id),
    FOREIGN KEY (hashtag_id) REFERENCES hashtags(id)
);

-- 5. Locations table (same)
CREATE TABLE  IF NOT EXISTS locations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tweet_id BIGINT,
    country VARCHAR(255),
    city VARCHAR(255),
    lat DOUBLE,
    lon DOUBLE,
    FOREIGN KEY (tweet_id) REFERENCES tweets(id)
);

-- 6. Sentiment Analysis (now includes detailed scores + multiple models)
CREATE TABLE  IF NOT EXISTS sentiments (
    tweet_id BIGINT PRIMARY KEY,
    sentiment_label VARCHAR(50),  -- positive, neutral, negative
    confidence_score FLOAT,
    emotion_label VARCHAR(50),    -- optional: anger, joy, sadness, etc.
    emotion_score FLOAT,
    FOREIGN KEY (tweet_id) REFERENCES tweets(id)
);

-- 7. Toxicity & Hate Speech Detection
CREATE TABLE IF NOT EXISTS  toxicity (
    tweet_id BIGINT PRIMARY KEY,
    toxicity_score FLOAT,         -- 0.0 to 1.0
    hate_speech_score FLOAT,      -- 0.0 to 1.0
    offensive_score FLOAT,        -- 0.0 to 1.0
    severe_toxicity_score FLOAT,  -- optional: intense hate
    FOREIGN KEY (tweet_id) REFERENCES tweets(id)
);

-- 8. Media Table (same)
CREATE TABLE IF NOT EXISTS  media (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tweet_id BIGINT,
    media_url TEXT,
    media_type VARCHAR(50), -- photo, video, gif
    FOREIGN KEY (tweet_id) REFERENCES tweets(id)
);

-- 9. Theme classification (NEW: tags related to your focus areas)
CREATE TABLE IF NOT EXISTS  tweet_themes (
    tweet_id BIGINT,
    theme_label VARCHAR(50), -- PwD, VAW, MentalHealth, LGBTQ
    model_confidence FLOAT,
    PRIMARY KEY (tweet_id, theme_label),
    FOREIGN KEY (tweet_id) REFERENCES tweets(id)
);
