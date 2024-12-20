# # # import win32evtlog
# # # import win32api
# # # import win32con
# # # import win32security  # To translate NT SIDs to account names.
# # # import win32evtlogutil
# # # import csv
# # # import sys
# # # import getopt

# # # def ReadLog(computer, logType="Application"):
# # #     """Read logs from the specified event log and return them as a list."""
# # #     logs = []
# # #     h = win32evtlog.OpenEventLog(computer, logType)
# # #     numRecords = win32evtlog.GetNumberOfEventLogRecords(h)

# # #     while True:
# # #         objects = win32evtlog.ReadEventLog(h, win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ, 0)
# # #         if not objects:
# # #             break
# # #         for obj in objects:
# # #             msg = win32evtlogutil.SafeFormatMessage(obj, logType)
# # #             sidDesc = None
# # #             if obj.Sid is not None:
# # #                 try:
# # #                     domain, user, typ = win32security.LookupAccountSid(computer, obj.Sid)
# # #                     sidDesc = f"{domain}/{user}"
# # #                 except win32security.error:
# # #                     sidDesc = str(obj.Sid)

# # #             log_entry = {
# # #                 "SourceName": obj.SourceName,
# # #                 "TimeGenerated": obj.TimeGenerated.Format(),
# # #                 "EventID": obj.EventID,
# # #                 "EventType": obj.EventType,
# # #                 "Message": msg,
# # #                 "User": sidDesc
# # #             }
# # #             logs.append(log_entry)

# # #     win32evtlog.CloseEventLog(h)
# # #     return logs

# # # def save_logs_to_csv(logs, output_file):
# # #     """Save logs to a CSV file."""
# # #     with open(output_file, mode="w", newline="", encoding="utf-8") as file:
# # #         fieldnames = ["SourceName", "TimeGenerated", "EventID", "EventType", "Message", "User"]
# # #         writer = csv.DictWriter(file, fieldnames=fieldnames)
# # #         writer.writeheader()
# # #         for log in logs:
# # #             writer.writerow(log)

# # # def usage():
# # #     print("Writes an event to the event log.")
# # #     print("-w : Don't write any test records.")
# # #     print("-r : Don't read the event log")
# # #     print("-c : computerName : Process the log on the specified computer")
# # #     print("-t : LogType - Use the specified log - default = 'Application'")

# # # def test():
# # #     # Check if running on Windows NT; if not, display notice and terminate
# # #     if win32api.GetVersion() & 0x80000000:
# # #         print("This sample only runs on NT")
# # #         return

# # #     opts, args = getopt.getopt(sys.argv[1:], "rwh?c:t:v")
# # #     computer = None
# # #     do_read = do_write = 1
# # #     logType = "Application"
    
# # #     if len(args) > 0:
# # #         print("Invalid args")
# # #         usage()
# # #         return 1
    
# # #     for opt, val in opts:
# # #         if opt == '-t':
# # #             logType = val
# # #         if opt == '-c':
# # #             computer = val
# # #         if opt in ['-h', '-?']:
# # #             usage()
# # #             return
# # #         if opt == '-r':
# # #             do_read = 0
# # #         if opt == '-w':
# # #             do_write = 0

# # #     if do_write:
# # #         ph = win32api.GetCurrentProcess()
# # #         th = win32security.OpenProcessToken(ph, win32con.TOKEN_READ)
# # #         my_sid = win32security.GetTokenInformation(th, win32security.TokenUser)[0]

# # #         # Write events to the event log
# # #         for event_type in [win32evtlog.EVENTLOG_INFORMATION_TYPE, win32evtlog.EVENTLOG_WARNING_TYPE]:
# # #             message_texts = [
# # #                 "The message text for event 2",
# # #                 "Another insert"
# # #             ] if event_type == win32evtlog.EVENTLOG_INFORMATION_TYPE else [
# # #                 "A warning",
# # #                 "An even more dire warning"
# # #             ]

# # #             win32evtlogutil.ReportEvent(logType, 1,
# # #                                          strings=message_texts,
# # #                                          data="Raw\0Data".encode("ascii"),
# # #                                          sid=my_sid,
# # #                                          eventType=event_type)

# # #         print("Successfully wrote events to the log")

# # #     if do_read:
# # #         logs = ReadLog(computer, logType)
# # #         save_logs_to_csv(logs, 'event_logs.csv')
# # #         print(f"Logs have been saved to 'event_logs.csv'")

# # # if __name__ == '__main__':
# # #     test()

# # import win32evtlog
# # import win32evtlogutil
# # import win32security
# # import csv

# # def read_logs(computer=None, log_type="Application"):
# #     """Read logs from the specified event log and return them as a list."""
# #     logs = []
# #     try:
# #         # Open the event log
# #         handle = win32evtlog.OpenEventLog(computer, log_type)
# #         flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ

# #         while True:
# #             events = win32evtlog.ReadEventLog(handle, flags, 0)
# #             if not events:
# #                 break  # Exit loop when no more logs are available

# #             for event in events:
# #                 try:
# #                     # Get log details
# #                     msg = win32evtlogutil.SafeFormatMessage(event, log_type)
# #                     sid_desc = None
# #                     if event.Sid:
# #                         try:
# #                             domain, user, _ = win32security.LookupAccountSid(computer, event.Sid)
# #                             sid_desc = f"{domain}/{user}"
# #                         except win32security.error:
# #                             sid_desc = "Unknown User"

# #                     log_entry = {
# #                         "SourceName": event.SourceName,
# #                         "TimeGenerated": event.TimeGenerated.Format(),
# #                         "EventID": event.EventID,
# #                         "EventType": event.EventType,
# #                         "Message": msg,
# #                         "User": sid_desc,
# #                     }
# #                     logs.append(log_entry)
# #                 except Exception as e:
# #                     print(f"Error processing event: {e}")
# #     except Exception as e:
# #         print(f"Error reading logs from {log_type}: {e}")
# #     finally:
# #         win32evtlog.CloseEventLog(handle)

# #     return logs

# # def save_logs_to_csv(logs, output_file="event_logs.csv"):
# #     """Save logs to a CSV file."""
# #     with open(output_file, mode="w", newline="", encoding="utf-8") as file:
# #         fieldnames = ["SourceName", "TimeGenerated", "EventID", "EventType", "Message", "User"]
# #         writer = csv.DictWriter(file, fieldnames=fieldnames)
# #         writer.writeheader()
# #         writer.writerows(logs)

# # def main():
# #     # Configure log source (e.g., Application, System, Security)
# #     log_type = "Application"  # Change this to "System" or "Security" if needed
# #     computer = None  # Replace with the computer name if connecting to a remote machine

# #     # Read logs
# #     logs = read_logs(computer, log_type)

# #     # Save to CSV if logs were collected
# #     if logs:
# #         save_logs_to_csv(logs, "event_logs.csv")
# #         print(f"Logs successfully saved to 'event_logs.csv'. Total logs: {len(logs)}")
# #     else:
# #         print("No logs were collected.")

# # if __name__ == "__main__":
# #     try:
# #         main()
# #     except KeyboardInterrupt:
# #         print("\nScript stopped.")

# import win32evtlog
# import win32evtlogutil
# import win32security
# import csv

# def read_logs(computer=None, log_types=["Application", "System", "Security"]):
#     """
#     Read logs from specified event log types.

#     Args:
#         computer (str): Target computer name, None for local logs.
#         log_types (list): List of log types to read (e.g., Application, System, Security).

#     Returns:
#         list: List of log entries.
#     """
#     logs = []
#     for log_type in log_types:
#         handle = None
#         try:
#             print(f"Opening log type: {log_type}")
#             # Open the event log
#             handle = win32evtlog.OpenEventLog(computer, log_type)
#             if not handle:
#                 print(f"Failed to open log type: {log_type}")
#                 continue

#             flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ

#             while True:
#                 try:
#                     events = win32evtlog.ReadEventLog(handle, flags, 0)
#                     if not events:
#                         break  # Exit loop when no more logs are available

#                     for event in events:
#                         try:
#                             # Format the message and user information
#                             msg = win32evtlogutil.SafeFormatMessage(event, log_type)
#                             sid_desc = None
#                             if event.Sid:
#                                 try:
#                                     domain, user, _ = win32security.LookupAccountSid(computer, event.Sid)
#                                     sid_desc = f"{domain}/{user}"
#                                 except win32security.error:
#                                     sid_desc = "Unknown User"

#                             log_entry = {
#                                 "LogType": log_type,
#                                 "SourceName": event.SourceName,
#                                 "TimeGenerated": event.TimeGenerated.Format(),
#                                 "EventID": event.EventID,
#                                 "EventType": event.EventType,
#                                 "Message": msg,
#                                 "User": sid_desc,
#                             }
#                             logs.append(log_entry)
#                         except Exception as e:
#                             print(f"Error processing event: {e}")
#                 except Exception as e:
#                     print(f"Error reading logs from {log_type}: {e}")
#                     break  # Exit loop on persistent errors
#         except Exception as e:
#             print(f"Error opening log {log_type}: {e}")
#         finally:
#             if handle:
#                 try:
#                     win32evtlog.CloseEventLog(handle)
#                 except Exception as e:
#                     print(f"Error closing log handle for {log_type}: {e}")
#     return logs

# def save_logs_to_csv(logs, output_file="all_event_logs.csv"):
#     """
#     Save logs to a CSV file.

#     Args:
#         logs (list): List of log entries.
#         output_file (str): Output CSV file name.
#     """
#     try:
#         with open(output_file, mode="w", newline="", encoding="utf-8") as file:
#             fieldnames = ["LogType", "SourceName", "TimeGenerated", "EventID", "EventType", "Message", "User"]
#             writer = csv.DictWriter(file, fieldnames=fieldnames)
#             writer.writeheader()
#             writer.writerows(logs)
#         print(f"Logs successfully saved to '{output_file}'. Total logs: {len(logs)}")
#     except Exception as e:
#         print(f"Error saving logs to CSV: {e}")

# def main():
#     # Define the log sources to read
#     log_types = ["Application", "System", "Security"]  # Add more sources if needed
#     computer = None  # Set to target computer name or None for local logs

#     print("Starting log collection...")
#     logs = read_logs(computer, log_types)

#     if logs:
#         save_logs_to_csv(logs, "all_event_logs.csv")
#     else:
#         print("No logs were collected.")

# if __name__ == "__main__":
#     try:
#         main()
#     except KeyboardInterrupt:
#         print("\nScript stopped.")

import win32evtlog
import win32evtlogutil
import win32security
import csv

def read_logs(computer=None, log_type="Application"):
    """
    Read logs from a specific event log type.

    Args:
        computer (str): Target computer name, None for local logs.
        log_type (str): The log type to read (e.g., Application, System, Security).

    Returns:
        list: List of log entries.
    """
    logs = []
    handle = None
    try:
        print(f"Opening log type: {log_type}")
        # Open the event log
        handle = win32evtlog.OpenEventLog(computer, log_type)
        if not handle:
            print(f"Failed to open log type: {log_type}")
            return logs

        flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ

        while True:
            try:
                events = win32evtlog.ReadEventLog(handle, flags, 0)
                if not events:
                    break  # Exit loop when no more logs are available

                for event in events:
                    try:
                        # Format the message and user information
                        msg = win32evtlogutil.SafeFormatMessage(event, log_type)
                        sid_desc = None
                        if event.Sid:
                            try:
                                domain, user, _ = win32security.LookupAccountSid(computer, event.Sid)
                                sid_desc = f"{domain}/{user}"
                            except win32security.error:
                                sid_desc = "Unknown User"

                        log_entry = {
                            "LogType": log_type,
                            "SourceName": event.SourceName,
                            "TimeGenerated": event.TimeGenerated.Format(),
                            "EventID": event.EventID,
                            "EventType": event.EventType,
                            "Message": msg,
                            "User": sid_desc,
                        }
                        logs.append(log_entry)
                    except Exception as e:
                        print(f"Error processing event: {e}")
            except Exception as e:
                print(f"Error reading logs from {log_type}: {e}")
                break  # Exit loop on persistent errors
    except Exception as e:
        print(f"Error opening log {log_type}: {e}")
    finally:
        if handle:
            try:
                win32evtlog.CloseEventLog(handle)
            except Exception as e:
                print(f"Error closing log handle for {log_type}: {e}")
    return logs

def save_logs_to_csv(logs, output_file):
    """
    Save logs to a CSV file.

    Args:
        logs (list): List of log entries.
        output_file (str): Output CSV file name.
    """
    try:
        with open(output_file, mode="w", newline="", encoding="utf-8") as file:
            fieldnames = ["LogType", "SourceName", "TimeGenerated", "EventID", "EventType", "Message", "User"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(logs)
        print(f"Logs successfully saved to '{output_file}'. Total logs: {len(logs)}")
    except Exception as e:
        print(f"Error saving logs to CSV: {e}")

def main():
    # Define the log sources
    log_types = ["Application", "System", "Security"]
    computer = None  # Set to target computer name or None for local logs

    print("Starting log collection...")
    for log_type in log_types:
        logs = read_logs(computer, log_type)
        if logs:
            output_file = f"{log_type}_logs.csv"
            save_logs_to_csv(logs, output_file)
        else:
            print(f"No logs collected for log type: {log_type}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nScript stopped.")
