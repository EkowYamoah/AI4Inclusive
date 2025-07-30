CREATE DATABASE TWEET_DATA;
USE TWEET_DATA;

-- 1. Users table (optional, but useful if user-level analysis is needed)
CREATE TABLE users (
    id BIGINT PRIMARY KEY,
    username VARCHAR(255),
    display_name VARCHAR(255),
    verified BOOLEAN,
    followers_count INT,
    following_count INT,
    location VARCHAR(255),
    created_at DATETIME
);

-- 2. Tweets table
CREATE TABLE tweets (
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

-- 3. Hashtags table
CREATE TABLE hashtags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    text VARCHAR(255) UNIQUE
);

-- 4. Tweet-Hashtag Join Table (many-to-many)
CREATE TABLE tweet_hashtags (
    tweet_id BIGINT,
    hashtag_id INT,
    PRIMARY KEY (tweet_id, hashtag_id),
    FOREIGN KEY (tweet_id) REFERENCES tweets(id),
    FOREIGN KEY (hashtag_id) REFERENCES hashtags(id)
);

-- 5. Locations table (optional if using geo-tagged tweets)
CREATE TABLE locations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tweet_id BIGINT,
    country VARCHAR(255),
    city VARCHAR(255),
    lat DOUBLE,
    lon DOUBLE,
    FOREIGN KEY (tweet_id) REFERENCES tweets(id)
);

-- 6. Sentiment Analysis Results (if integrated)
CREATE TABLE sentiments (
    tweet_id BIGINT PRIMARY KEY,
    sentiment_label VARCHAR(50), -- e.g., positive, negative, neutral
    confidence_score FLOAT,
    FOREIGN KEY (tweet_id) REFERENCES tweets(id)
);

-- 7. Media Table (for tweets with media attachments)
CREATE TABLE media (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tweet_id BIGINT,
    media_url TEXT,
    media_type VARCHAR(50), -- photo, video, gif
    FOREIGN KEY (tweet_id) REFERENCES tweets(id)
);
