-- # List all targets that the Application Load Balancer routes traffic to and the number of routed requests per target, by percentage distribution 
SELECT target_ip, (Count(target_ip)* 100.0 / (Select Count(*) From alb_logs))
    as backend_traffic_percentage
FROM alb_logs
GROUP by target_ip<
ORDER By count() DESC;