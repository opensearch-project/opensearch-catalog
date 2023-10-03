-- # List clients, in descending order, by the number of times that each client visited a specified URL
SELECT client_ip, elb, request_url, count(*) as count from alb_logs
GROUP by client_ip, elb, request_url
ORDER by count DESC;