import argparse
import time
import os
import json
import re
from user_agents import parse as ua_parse
import pandas as pd


# Initialize the argument parser
parser = argparse.ArgumentParser(description='ETL script for processing log files.')
parser.add_argument('--filename', type=str, default='apache_logs.txt', help='Filename for the raw log file to process.')

# Parse the arguments
args = parser.parse_args()

# Function to follow the tail of a log file
def follow(filename):
    with open(filename, 'r') as f:
        # Move to the end of the file
        f.seek(0, os.SEEK_END)

        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1)  # Sleep briefly to avoid busy waiting
                continue
            yield line

# Define a regular expression pattern for Apache logs
log_pattern = re.compile(
    r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[(?P<timestamp>[^\]]+)\] "(?P<method>\w+) (?P<url>[^\s]+) HTTP/(?P<flavor>[^"]+)" (?P<status_code>\d+) (?P<bytes>\d+) "(?P<referer>[^"]+)" "(?P<user_agent>[^"]+)"'
)

# Function to parse and transform a single log line
def parse_and_transform_log_line(line):
    match = log_pattern.match(line)
    if match:
        user_agent = ua_parse(match.group('user_agent'))
        log_json = {
            "observedTimestamp": pd.to_datetime(match.group('timestamp'), format='%d/%b/%Y:%H:%M:%S %z').strftime('%Y-%m-%dT%H:%M:%S.000Z'),
            "http": {
                "response": {
                    "status_code": int(match.group('status_code')),
                    "bytes": int(match.group('bytes'))
                },
                "url": match.group('url'),
                "flavor": match.group('flavor'),
                "request": {
                    "method": match.group('method')
                },
                "user_agent": {
                    "original": match.group('user_agent'),
                    "name": user_agent.browser.family,
                    "version": user_agent.browser.version_string,
                    "os": {
                        "name": user_agent.os.family,
                        "full": user_agent.os.family + " " + user_agent.os.version_string,
                        "version": user_agent.os.version_string,
                        "device": {
                            "name": user_agent.device.family
                        }
                    }
                }
            },
            "communication": {
                "source": {
                    "address": match.group('ip'),
                    "ip": match.group('ip'),
                    "geo": {
                        "country": "",  # Add this if you have the data
                        "country_iso_code": ""  # Add this if you have the data
                    }
                }
            },
            "body": line,
            "traceId": "",  # Add this if you have the data
            "spanId": "",  # Add this if you have the data
            "@timestamp": pd.to_datetime(match.group('timestamp'), format='%d/%b/%Y:%H:%M:%S %z').strftime('%Y-%m-%dT%H:%M:%S.000Z')
        }
        return log_json
    else:
        return None
def main(logfile_path):
    loglines = follow(logfile_path)

    # Open the output file in append mode
    with open('output_log.json', 'a') as outfile:
        # Process each incoming log line
        for line in loglines:
            log_json = parse_and_transform_log_line(line)
            if log_json:
                # Write the JSON to the file
                outfile.write(json.dumps(log_json) + '\n')
                outfile.flush()

if __name__ == "__main__":
    # Initialize the argument parser
    parser = argparse.ArgumentParser(description='ETL script for processing log files.')
    parser.add_argument('--filename', type=str, default='apache_logs.txt', help='Filename for the raw log file to process.')

    # Parse the arguments
    args = parser.parse_args()

    # Run the main function
    main(args.filename)