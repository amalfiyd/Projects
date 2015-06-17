CREATE VIEW majority_turkratings_2 AS
SELECT a.topics as topics, a.timestamp as timestamp, b.count
FROM topic_ratings as a
INNER JOIN topic_tweets as b
ON a.topics = b.topics
WHERE a.major_rating = 2

CREATE VIEW majority_turkratings_2_preprocessed_d AS
SELECT DAY(timestamp) as my_day, MONTH(timestamp) as my_month, YEAR(timestamp) as my_year, SUM(count) as my_count
FROM majority_turkratings_2
GROUP BY my_day
ORDER BY timestamp ASC

CREATE VIEW `threshold_group_count` AS 
select `a`.`topics` AS `topics`,`a`.`timestamp` AS `timestamp`,`b`.`count` AS `count`,`a`.`threshold_group` AS `threshold_group` 
from (`topic_ratings` `a` join `topic_tweets` `b` on((`a`.`topics` = `b`.`topics`))) 
order by `a`.`threshold_group`;

CREATE VIEW `temp` AS
SELECT WEEK(timestamp) as my_week, SUM(count) as my_count, threshold_group
FROM `threshold_group_count`
GROUP BY my_week, threshold_group
ORDER BY threshold_group, timestamp ASC