CREATE COVERING INDEX ON "ss4o_logs-aws_elb"
WITH (
  auto_refresh = true,
  refresh_interval = '1 day',
  checkpoint_location = 's3://test/'
)