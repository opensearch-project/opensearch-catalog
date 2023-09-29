-- # List clients, in descending order, by the amount of data (in megabytes) that each client sent in their requests to the Application Load Balancer
SELECT client_ip, sum(received_bytes/1000000.0) as client_datareceived_megabytes
FROM alb_logs
GROUP by client_ip
ORDER by client_datareceived_megabytes DESC;