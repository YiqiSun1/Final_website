-- Enable RUM extension for full-text search
CREATE EXTENSION IF NOT EXISTS rum;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(64) NOT NULL UNIQUE,
    email VARCHAR(128) NOT NULL UNIQUE,
    password_hash VARCHAR(128) NOT NULL
);

-- Create index on email for faster lookups
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);

-- Tweets table
CREATE TABLE IF NOT EXISTS tweets (
    id SERIAL PRIMARY KEY,
    content VARCHAR(280) NOT NULL,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    content_tsv tsvector GENERATED ALWAYS AS (to_tsvector('english', content)) STORED
);

-- Create index on user_id for faster lookups of user's tweets
CREATE INDEX IF NOT EXISTS idx_tweets_user_id ON tweets(user_id);
-- Create RUM index for full-text search (replacing GIN)
CREATE INDEX IF NOT EXISTS idx_tweets_content_rum ON tweets USING rum (content_tsv);

-- id_urls table referencing tweets.id
CREATE TABLE IF NOT EXISTS id_urls (
    id BIGSERIAL PRIMARY KEY,
    tweet_id INTEGER REFERENCES tweets(id) ON DELETE CASCADE,
    url TEXT
);
