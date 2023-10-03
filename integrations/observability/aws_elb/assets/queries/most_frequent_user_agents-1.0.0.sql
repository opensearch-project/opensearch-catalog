-- # List the ? (10) URLs that ? (Firefox) users accessed most frequently, in descending order
SELECT request_url, user_agent, count(*) as count
FROM alb_logs
WHERE user_agent LIKE '%?%'
GROUP by request_url, user_agent
ORDER by count(*) DESC LIMIT ?;