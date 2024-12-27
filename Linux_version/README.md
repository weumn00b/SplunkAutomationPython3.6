# Splunk Automation - Linux version   

## Overview  
This project automates the collection of system logs (Application, Security, and System) from a Linux machine and uploads them to a Splunk server for further analysis. The scripts extract logs using native Linux tools (`journalctl` and `dmesg`) and send them to Splunk over a TCP connection.  

---

## How It Works  
1. **Log Extraction** – The scripts extract logs using system commands:  
   - **Application logs** – Collected via `journalctl` (priority 4 and above).  
   - **Security logs** – Extracts logs from services like SSH using `journalctl -u ssh`.  
   - **System logs** – Kernel and boot messages are captured using `dmesg`.  

2. **Log Forwarding** – Logs are sent to the Splunk server using a TCP socket connection in JSON format.  

3. **Retries & Error Handling** – If a log fails to send, the script retries the connection with exponential backoff up to 5 times.  

4. **Automation** – A `main.py` script runs all log extraction scripts in one go.  

---

## File Descriptions  

### 1. **application_log.py**  
- **Purpose**: Extracts general application logs and sends them to Splunk.  
- **Command**: `journalctl -p 4 --since yesterday` – Retrieves logs with priority 4 (warning) and above from the last 24 hours.  

---

### 2. **security_log.py**  
- **Purpose**: Collects SSH and authentication-related logs.  
- **Command**: `journalctl -u ssh --since yesterday` – Extracts SSH-related logs from the last 24 hours.  

---

### 3. **system_log.py**  
- **Purpose**: Extracts system logs, kernel messages, and boot logs.  
- **Command**: `dmesg` – Retrieves all kernel logs since boot.  

---

### 4. **main.py**  
- **Purpose**: Executes all three scripts (`application_log.py`, `security_log.py`, and `system_log.py`) in sequence.  
- **Command**: Runs each script through `subprocess.run()`.  

---

## Setup  

### 1. **Requirements**  
Ensure the following are installed on the Linux machine:  
- **Python 3.x** – Required to run the scripts.  
- **Systemd Journal (journalctl)** – Extracts logs from system services.  
- **Git** – To clone the repository.  
- **Splunk Server** – Running and configured to receive logs over TCP.  

---

### 2. **Installation**  

1. **Install Required Packages**:  
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip git
   ```  

2. **Clone the Repository**:  
   ```bash
   git clone https://github.com/AbdinasirM/SplunkAutomation
   cd SplunkAutomation
   ```  

3. **Install Python Dependencies**:  
   ```bash
   pip install -r requirements.txt
   ```  

---

### 3. **Configuring Splunk to Receive Logs**  

1. **On the Splunk Server**:  
   - Go to **Settings** -> **Data Inputs** -> **TCP** -> **New Local TCP**.  
   - Set the **Port** to match the one used in the Python scripts (e.g., 9000).  
   - **Source Name Override** – Optional to label the input.  
   - Click **Next**.  

2. **Select Source Type**:  
   - In the dropdown, select **Operating System**.  
   - Choose **linux_secure_logs** or **linux_syslog**.  

3. **Host Configuration**:  
   - Enter the IP of the Linux machine.  
   - Change from DNS to **IP**.  

4. **Review and Submit**:  
   - Click **Review**.  
   - Verify configurations and click **Submit**.  

---

### 4. **Running the Scripts**  

- **To run all scripts at once**:  
   ```bash
   sudo python3 main.py
   ```  
- **To run individual scripts**:  
   ```bash
   sudo python3 application_log.py
   sudo python3 security_log.py
   sudo python3 system_log.py
   ```  

---


(No external dependencies needed, but ensure Python 3 and journalctl are available.)  

---

## Additional Notes  

1. **Security Logs** – The `security_log.py` script requires `sudo` to access SSH and authentication logs.  

2. **Error Handling** –  
   - If Splunk is unreachable, the scripts retry up to 5 times with exponential backoff.  
   - Errors during log collection are printed to the console for debugging.  

3. **Splunk Configuration** –  
   - Ensure Splunk is running and accessible over the network at the configured IP and port.  

4. **Customization** –  
   - Update the `SPLUNK_SERVER_IP` and `SPLUNK_SERVER_PORT` variables in each script to match your Splunk server settings.  

