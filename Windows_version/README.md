# Splunk Automation - Windows version  

## Overview  
This project automates the extraction of Windows Event Logs (Application, Security, and System logs) and uploads them to a Splunk server for further analysis. Each log type has its own Python script (`application_log.py`, `security_log.py`, `system_log.py`), which reads the logs, processes them, and sends them to a configured Splunk server. The project also includes a `main.py` file to run all scripts at once.  

---

## How It Works  
1. **Log Reading** – Each script reads its respective Windows Event Log using the `win32evtlog` library.  
2. **Log Filtering** – Only new logs (not previously uploaded) are sent to the Splunk server. Timestamps of the last uploaded logs are stored in a CSV file.  
3. **Log Uploading** – Logs are sent to the Splunk server using sockets. The scripts retry failed uploads with exponential backoff.  
4. **Administrator Privileges** – Running `main.py` or `security_log.py` requires **Administrator privileges** to access Security logs.  

---

## Setup  

### 1. **Requirements**  
Ensure the following are installed on the client Windows machine before running the scripts:  

- **Python 3.x** – Required to execute the Python scripts. Download from [python.org](https://www.python.org/downloads/).  
- **Git** – To clone the repository. Download from [git-scm.com](https://git-scm.com/downloads).  
- **Splunk Server** – Must be running and configured to receive logs over the specified IP and port.  

---

### 2. **Installation**  
1. Clone the repository using Git:  
   ```bash
   git clone https://github.com/AbdinasirM/SplunkAutomation
   cd SplunkAutomation
   ```  
2. Install Python dependencies:  
   ```bash
   pip install -r requirements.txt
   ```  
3. Update the following variables in each script if necessary:  
   - `SPLUNK_SERVER_IP` – IP address of your Splunk server.  
   - `SPLUNK_SERVER_PORT` – Port of your Splunk server.  

4. **Run `main.py` with Administrator Command Prompt** to ensure Security logs can be processed.  

---

### 3. **Configuring Splunk to Receive Logs**  

To allow the Splunk server to receive TCP logs from the Windows client:  

1. **On the Splunk Server:**   
   - Go to **Settings** -> **Data Inputs** -> **TCP** -> **New Local TCP**.  

2. **Create a TCP Port for Data Input:**   
   - Set the **Port** number to the one you will use in the Python scripts (e.g., 9000).   
   - Optionally, set a **Source Name Override** to identify this input.  
   - Click **Next**.  

3. **Select Source Type:**   
   - In the “Select Source Type” dropdown, choose **Operating System**.  
   - Scroll down and select **windows_snare_logs** as the source type.  

4. **Host Configuration:**   
   - Set the **IP** of the host machine sending the logs.  
   - Change the default DNS setting to **IP** to ensure proper log identification.  

5. **Review and Submit:**   
   - Click **Review**.  
   - Verify all settings and click **Submit**.  

---

### 4. **Running the Scripts**  

- **Run `main.py` to execute all scripts at once** and upload Application, Security, and System logs:  
   ```bash
   python main.py
   ```  
- **Security Log** – `main.py` must be executed with **Administrator Command Prompt** to process Security logs properly.  
- Alternatively, you can run individual scripts if needed:  
   ```bash
   python application_log.py
   python security_log.py  # Requires Administrator Command Prompt
   python system_log.py
   ```  

---

## File Descriptions  

### 1. **application_log.py**  
**Purpose**: Reads and uploads logs from the "Application" log in Windows Event Viewer.  

**How It Works**:  
- Opens the Application log using `win32evtlog`.  
- Reads events sequentially and filters out logs already uploaded (based on timestamps stored in `application_log_last_eventuploaded.csv`).  
- Sends new logs to the Splunk server using a socket connection.  
- Handles upload failures with retries and exponential backoff.  
- Updates the CSV file with the timestamp of the latest uploaded event.  

---

### 2. **security_log.py**  
**Purpose**: Reads and uploads logs from the "Security" log in Windows Event Viewer.  

**How It Works**:  
- Similar to `application_log.py`, but operates on the "Security" log.  
- The timestamp of the last uploaded log is stored in `security_log_last_eventuploaded.csv`.  
- **Must be run with Administrator privileges** due to restricted access to Security logs.  

---

### 3. **system_log.py**  
**Purpose**: Reads and uploads logs from the "System" log in Windows Event Viewer.  

**How It Works**:  
- Similar to `application_log.py`, but operates on the "System" log.  
- Tracks uploaded logs using `system_log_last_eventuploaded.csv`.  

---

### 4. **main.py**  
**Purpose**: Acts as an entry point for running all log scripts at once.  

**How It Works**:  
- Executes `application_log.py`, `security_log.py`, and `system_log.py` in sequence.  
- Ensures Administrator privileges are set for processing Security logs.  
- Provides a consolidated way to manage execution.  

---

## Requirements File (`requirements.txt`)  

```plaintext
pywin32
```  
**Explanation**:  
- `pywin32` – Required for accessing Windows Event Logs through Python.  

---

## Additional Notes  

1. **CSV Files** – Each script generates a CSV file to track the last uploaded event's timestamp:  
   - `application_log_last_eventuploaded.csv`  
   - `security_log_last_eventuploaded.csv`  
   - `system_log_last_eventuploaded.csv`  

2. **Error Handling** –  
   - Scripts retry failed uploads with a maximum of 5 attempts.  
   - Exponential backoff is implemented to avoid overwhelming the server.  

3. **Administrator Privileges** –  
   - The Security logs script (`security_log.py`) requires **Administrator privileges** to access restricted logs.  

4. **Splunk Configuration** –  
   - Ensure your Splunk server is running and configured to accept logs over the specified IP and port.  
