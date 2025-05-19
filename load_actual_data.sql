-- Insert 1,000,000 users
INSERT INTO users (username, email, password_hash)
SELECT
    'user_' || i,
    'user_' || i || '@sportsmail.com',
    'hashed_pw_' || i
FROM generate_series(1, 1000000) AS i;

-- Create temp tables for sports + sentiments
CREATE TEMP TABLE sports(word TEXT);
INSERT INTO sports(word) VALUES 
('soccer'), ('basketball'), ('tennis'), ('cricket'), ('baseball'),
('golf'), ('hockey'), ('rugby'), ('F1'), ('MMA'),
('surfing'), ('skiing'), ('boxing'), ('swimming'), ('cycling');

CREATE TEMP TABLE sentiments(phrase TEXT);
INSERT INTO sentiments(phrase) VALUES 
('I love'), ('I hate'), ('I enjoy watching'), ('I never miss'), ('I can’t stand');

-- Insert 10,000,000 tweets
INSERT INTO tweets (content, user_id)
SELECT 
    s.phrase || ' ' || sp.word,
    FLOOR(RANDOM() * 1000000 + 1)::INT
FROM generate_series(1, 10000000), sentiments s, sports sp
LIMIT 10000000;

-- Randomly assign URLs to 1–5 million tweets
INSERT INTO id_urls (tweet_id, url)
SELECT 
    id,
    'https://example.com/sports/' || id
FROM tweets
WHERE RANDOM() < 0.3;  -- ~30% get URLs (adjust as needed)
