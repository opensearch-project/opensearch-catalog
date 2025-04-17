# Apache Log Processor

This folder contains scripts for processing Apache log files and transforming them into a JSON format suitable for ingestion into an OpenSearch Apache based SS4O index.

## Scripts

### `generator.py`

This script simulates a live Apache log file. It continuously generates log entries and appends them to a specified file.

#### Arguments

- `--filename`: The filename where the generated logs will be stored. Default is `apache_logs.txt`.

### `run-etl.py`

This script reads from a live Apache log file, transforms each log entry into a structured JSON format, and appends the output to a file called `output_log.json`.

#### Arguments

- `--filename`: The filename of the raw Apache log file to process. Default is `apache_logs.txt`.

## Usage

### Running
To use these scripts, you will need Python installed on your system along with the necessary packages listed in `requirements.txt`.

The next `run.sh` bash script is designed to orchestrate the execution of two Python scripts: `generator.py` and `run-etl.py`, which are involved in generating and processing Apache log data, respectively.
The script also ensures that the necessary Python dependencies are installed by using a requirements.txt file. Here's a breakdown of its functionality:

```bash
./run.sh --filename apache_raw.logs
```
Dont forget allowing the script to run by adding the next file premissions

```text
chmod +x run.sh
```

### Stopping

Stopping the background processes is done using the `stop.sh` script

```bash
./stop.sh 
```

Don't forget allowing the script to run by adding the next file premissions

```text
chmod +x stop.sh
```

### Sync the result to S3 bucket
To synchronizes a JSON file to an Amazon S3 bucket based on provided arguments for the file name and the S3 bucket name, you'll need to use the AWS Command Line Interface (AWS CLI).
Make sure you have AWS CLI installed and configured with the necessary credentials and permissions to write to the S3 bucket.

Dont forget allowing the script to run by adding the next file premissions

```text
chmod +x sync_s3.sh
```

You can then run the script by providing the filename and the S3 bucket name:

```bash
./sync_s3.sh --filename output_log.json --bucket s3://my_data/apache_logs
```