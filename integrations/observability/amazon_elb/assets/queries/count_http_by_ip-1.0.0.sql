-- # Count the number of HTTP GET requests received by the load balancer grouped by the client IP address
SELECT COUNT(request_verb)
    AS count, request_verb, client_ip
FROM alb_logs_partitioned
WHERE day = '?'
GROUP by request_verb, client_ip;