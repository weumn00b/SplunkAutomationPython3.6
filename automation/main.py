# import subprocess
# import time
# import csv
# from datetime import datetime, timedelta

# def get_last_event_time(csv_file):
#     try:
#         with open(csv_file, mode="r") as csvfile:
#             reader = csv.reader(csvfile)
#             return datetime.strptime(next(reader)[0], "%Y-%m-%d %H:%M:%S")
#     except Exception:
#         return None

# def check_and_run():
#     files = [
#         ("system_log.py", "system_log_last_eventuploaded.csv"),
#         ("security_log.py", "security_log_last_eventuploaded.csv"),
#         ("application_log.py", "application_log_last_eventuploaded.csv"),
#     ]

#     for script, csv_file in files:
#         last_event_time = get_last_event_time(csv_file)
#         if not last_event_time or datetime.now() - last_event_time >= timedelta(minutes=1):
#             subprocess.Popen(["python", script])

# if __name__ == "__main__":
#     while True:
#         check_and_run()
#         time.sleep(30)
import subprocess
import time
import csv
from datetime import datetime, timedelta
import os

# Define log scripts and their corresponding CSV files
LOG_SCRIPTS = [
    ("system_log.py", "system_log_last_eventuploaded.csv"),
    ("security_log.py", "security_log_last_eventuploaded.csv"),
    ("application_log.py", "application_log_last_eventuploaded.csv"),
]

# Function to get the last event time from CSV
def get_last_event_time(csv_file):
    try:
        with open(csv_file, mode="r") as csvfile:
            reader = csv.reader(csvfile)
            return datetime.strptime(next(reader)[0], "%a %b %d %H:%M:%S %Y")
    except (FileNotFoundError, StopIteration):
        return None  # Return None if CSV does not exist or is empty

# Function to run log script if needed
def check_and_run():
    for script, csv_file in LOG_SCRIPTS:
        last_event_time = get_last_event_time(csv_file)
        
        # If no last event time, perform full upload (first run)
        if last_event_time is None:
            print(f"Running full upload for {script} (first run).")
            subprocess.Popen(["python", script])
        
        # If last event is older than 1 minute, run incremental upload
        elif datetime.now() - last_event_time >= timedelta(minutes=1):
            print(f"Running incremental upload for {script}.")
            subprocess.Popen(["python", script])
        else:
            print(f"{script} has no new logs to upload. Skipping this run.")

if __name__ == "__main__":
    print("Log monitoring started. Running checks every 60 seconds...")
    while True:
        check_and_run()
        time.sleep(60)
