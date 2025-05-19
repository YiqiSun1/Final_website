-- Enable pgcrypto for password hashing
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Insert 100 users
INSERT INTO users (username, email, password_hash)
SELECT 
    'user_' || i,
    'user_' || i || '@example.com',
    encode(digest('password' || i, 'sha256'), 'hex')
FROM generate_series(1, 100) AS s(i);

-- Insert 100 tweets
INSERT INTO tweets (content, user_id, created_at)
SELECT 
    'This is tweet #' || i || ' about random topic ' || md5(random()::text),
    (SELECT id FROM users ORDER BY random() LIMIT 1),
    NOW() - (i || ' minutes')::INTERVAL
FROM generate_series(1, 100) AS s(i);

-- Insert 100 URLs
INSERT INTO id_urls (tweet_id, url)
SELECT 
    (SELECT id FROM tweets ORDER BY random() LIMIT 1),
    'https://example.com/page/' || i
FROM generate_series(1, 100) AS s(i);
