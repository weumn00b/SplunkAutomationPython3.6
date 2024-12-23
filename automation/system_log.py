import win32evtlog
import win32evtlogutil
import socket
import json
import csv
from datetime import datetime

SPLUNK_SERVER_IP = "localhost"
SPLUNK_SERVER_PORT = 9000
LOG_TYPE = "System"
CSV_FILE = "system_log_last_eventuploaded.csv"

def send_to_splunk(log_entry):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((SPLUNK_SERVER_IP, SPLUNK_SERVER_PORT))
            sock.sendall(json.dumps(log_entry).encode('utf-8'))
        print(f"Sent log to Splunk: {log_entry}")
    except Exception as e:
        print(f"Error sending log to Splunk: {e}")

def get_last_event_time():
    try:
        with open(CSV_FILE, mode="r") as csvfile:
            reader = csv.reader(csvfile)
            return next(reader)[0]  # Return the first row (date)
    except Exception:
        return None  # Return None if the CSV doesn't exist

def save_last_event_time(event_time):
    with open(CSV_FILE, mode="w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([event_time])  # Save the latest event time to CSV

def read_logs():
    last_uploaded = get_last_event_time()
    handle = None
    latest_event_time = None

    try:
        handle = win32evtlog.OpenEventLog(None, LOG_TYPE)
        flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ

        while True:
            events = win32evtlog.ReadEventLog(handle, flags, 0)
            if not events:
                break

            for event in events:
                time_generated = event.TimeGenerated.Format()
                event_dt = datetime.strptime(time_generated, "%a %b %d %H:%M:%S %Y")

                # Upload all logs if no date is saved in CSV
                if last_uploaded:
                    last_uploaded_dt = datetime.strptime(last_uploaded, "%a %b %d %H:%M:%S %Y")
                    if event_dt <= last_uploaded_dt:
                        continue  # Skip logs already uploaded

                log_entry = {
                    "LogType": LOG_TYPE,
                    "SourceName": event.SourceName,
                    "TimeGenerated": time_generated,
                    "EventID": event.EventID,
                    "EventType": event.EventType,
                    "Message": win32evtlogutil.SafeFormatMessage(event, LOG_TYPE),
                }
                send_to_splunk(log_entry)

                # Track the most recent event processed
                if not latest_event_time or event_dt > latest_event_time:
                    latest_event_time = event_dt

    except Exception as e:
        print(f"Error processing {LOG_TYPE} logs: {e}")
    finally:
        if handle:
            win32evtlog.CloseEventLog(handle)

        # Save the latest event time if new events were processed
        if latest_event_time:
            save_last_event_time(latest_event_time.strftime("%a %b %d %H:%M:%S %Y"))

if __name__ == "__main__":
    read_logs()
