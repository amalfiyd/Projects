CREATE VIEW majority_turkratings_2 AS
SELECT a.topics as topics, a.timestamp as timestamp, b.count
FROM topic_ratings as a
INNER JOIN topic_tweets as b
ON a.topics = b.topics
WHERE a.major_rating = 2

CREATE VIEW majority_turkratings_2_preprocessed AS
SELECT WEEK(timestamp) as my_week, MONTH(timestamp) as my_month, YEAR(timestamp) as my_year, SUM(count) as my_count
FROM majority_turkratings_2
GROUP BY my_week
ORDER BY timestamp ASC
