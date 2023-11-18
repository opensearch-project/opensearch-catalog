import argparse
from faker import Faker
import random

# Initialize Faker
fake = Faker()

# Set up command-line argument parsing
parser = argparse.ArgumentParser(description='Generate Apache log files with Faker.')
parser.add_argument('--filename', type=str, default='apache_logs.txt', help='Filename for the generated log file.')
parser.add_argument('--log-number', type=int, default=1000, help='Number of logs to generate.')
parser.add_argument('--start-time', type=str, help='Start time for log generation in YYYY-MM-DD format.')
parser.add_argument('--end-time', type=str, help='End time for log generation in YYYY-MM-DD format.')

args = parser.parse_args()

# Define the log format
log_format = '{ip} - - [{time}] "{method} {url} HTTP/1.1" {status_code} {size} "{referer}" "{user_agent}"'

# Generate logs with the provided parameters
with open(args.filename, 'w') as log_file:
    for _ in range(args.log_number):
        # If time range is provided, generate logs within that range
        if args.start_time and args.end_time:
            time = fake.date_time_between(start_date=args.start_time, end_date=args.end_time).strftime('%d/%b/%Y:%H:%M:%S +0000')
        else:
            time = fake.date_time().strftime('%d/%b/%Y:%H:%M:%S +0000')

        log_entry = log_format.format(
            ip=fake.ipv4(),
            time=time,
            method=random.choice(['GET', 'POST', 'DELETE', 'PUT']),
            url=fake.uri_path(),
            status_code=random.choice([200, 301, 400, 404, 500]),
            size=random.randint(20, 5000),
            referer=fake.uri(),
            user_agent=fake.user_agent()
        )
        print(log_entry, file=log_file)

print(f"Generated {args.log_number} log entries in {args.filename}")
