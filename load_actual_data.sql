-- Enable pgcrypto for password hashing
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- ========================
-- STEP 1: Insert 1,000,000 Users
-- ========================
INSERT INTO users (username, email, password_hash)
SELECT 
    'user_' || i,
    'user_' || i || '@example.com',
    encode(digest('password' || i, 'sha256'), 'hex')
FROM generate_series(1, 1000000) AS s(i)
ON CONFLICT (username) DO NOTHING;

-- ========================
-- STEP 2: Insert 10,000,000 Tweets (random user_id)
-- ========================
INSERT INTO tweets (content, user_id, created_at)
SELECT 
    'Tweet #' || i || ' - ' || md5(random()::text),
    (SELECT id FROM users ORDER BY random() LIMIT 1),
    NOW() - (random() * INTERVAL '30 days')
FROM generate_series(1, 10000000) AS s(i);

-- ========================
-- STEP 3: Insert 10,000,000 id_urls (random tweet_id)
-- ========================
INSERT INTO id_urls (tweet_id, url)
SELECT 
    (SELECT id FROM tweets ORDER BY random() LIMIT 1),
    'https://example.com/resource/' || i
FROM generate_series(1, 10000000) AS s(i);
