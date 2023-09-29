-- # List each time in a specified date range when the target processing time was more than ? (5) seconds
SELECT * from alb_logs
WHERE (parse_datetime(time,'yyyy-MM-dd''T''HH:mm:ss.SSSSSS''Z')
    BETWEEN parse_datetime('?','?')
    AND parse_datetime('?','?'))
  AND (target_processing_time >= ?);