import argparse
from faker import Faker
import random
import time

def main():
    fake = Faker()

    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description='Generate Apache log files with Faker.')
    parser.add_argument('--filename', type=str, default='apache_logs.txt', help='Filename for the generated log file.')
    parser.add_argument('--log-number', type=int, default=-1, help='Number of logs to generate. Pass a negative number to generate logs indefinitely.')
    parser.add_argument('--start-time', type=str, help='Start time for log generation in YYYY-MM-DD format.')
    parser.add_argument('--end-time', type=str, help='End time for log generation in YYYY-MM-DD format.')

    args = parser.parse_args()

    # Define the log format
    log_format = '{ip} - - [{time}] "{method} {url} HTTP/1.1" {status_code} {size} "{referer}" "{user_agent}"'

    # Open the log file
    with open(args.filename, 'w') as log_file:
        log_count = 0  # Initialize a counter for the number of logs generated
        while args.log_number < 0 or log_count < args.log_number:
            # If time range is provided, generate logs within that range
            if args.start_time and args.end_time:
                time_str = fake.date_time_between(start_date=args.start_time, end_date=args.end_time).strftime('%d/%b/%Y:%H:%M:%S +0000')
            else:
                time_str = fake.date_time().strftime('%d/%b/%Y:%H:%M:%S +0000')

            log_entry = log_format.format(
                ip=fake.ipv4(),
                time=time_str,
                method=random.choice(['GET', 'POST', 'DELETE', 'PUT']),
                url=fake.uri_path(),
                status_code=random.choice([200, 301, 400, 404, 500]),
                size=random.randint(20, 5000),
                referer=fake.uri(),
                user_agent=fake.user_agent()
            )
            print(log_entry, file=log_file)
            log_count += 1
            # To avoid high CPU usage, add a small delay in the infinite loop
            if args.log_number < 0:
                time.sleep(0.1)  # Sleep for 0.1 second

    # Print out how many log entries were generated
    if args.log_number < 0:
        print(f"Generated logs indefinitely in {args.filename}")
    else:
        print(f"Generated {log_count} log entries in {args.filename}")

if __name__ == "__main__":
    main()
