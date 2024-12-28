# Splunk Automation - Linux Version  

## Overview  
This project automates the collection of logs (Application, Security, and System) from a Linux machine and sends them to a Splunk server for analysis. The scripts use Linux tools (`journalctl` and `dmesg`) to gather logs and forward them to Splunk over TCP.  

---

## How It Works  
1. **Log Collection**  
   - **Application logs** – General system app logs (`journalctl`).  
   - **Security logs** – SSH and login logs (`journalctl -u ssh`).  
   - **System logs** – Kernel and boot logs (`dmesg`).  

2. **Log Forwarding**  
   - Logs are formatted in JSON and sent to the Splunk server using TCP.  

3. **Error Handling**  
   - If the Splunk server is unreachable, the script retries 5 times.  

4. **Automation**  
   - A `main.py` script runs all log scripts automatically.  

---

## Files and What They Do  

### 1. **application_log.py**  
- **Purpose**: Collects application logs (warnings and errors).  
- **Command**:  
   ```bash
   journalctl -p 4 --since yesterday
   ```  
   - Priority 4 = Warnings and higher.  

---

### 2. **security_log.py**  
- **Purpose**: Collects security logs (SSH, login attempts).  
- **Command**:  
   ```bash
   journalctl -u ssh --since yesterday
   ```  

---

### 3. **system_log.py**  
- **Purpose**: Collects system and kernel logs.  
- **Command**:  
   ```bash
   dmesg
   ```  

---

### 4. **main.py**  
- **Purpose**: Runs all scripts (application, security, system) in sequence.  
- **Command**: Runs each script every minute.  

---

## Setup  

### 1. **Requirements**  
Ensure the following are installed on the client Linux machine before running the scripts:  

- **Python 3.x** – Required to execute the Python scripts. Download from [python.org](https://www.python.org/downloads/).  
- **Git** – To clone the repository. Download from [git-scm.com](https://git-scm.com/downloads).  
- **Splunk Server** – Must be running and configured to receive logs over the specified IP and port.  

---

### 2. Install Python and Required Tools  
Open your terminal and run:  
```bash
sudo apt update
sudo apt install python3 python3-pip git
```

---

### 3. Download the Project  
Clone the project from GitHub:  
```bash
git clone https://github.com/AbdinasirM/SplunkAutomation
cd SplunkAutomation/linux
```

---

### 4. Configure Splunk to Accept Logs  

1. Log into Splunk Web Interface:  
   ```bash
   http://<splunk-server-ip>:8000
   ```  
2. Go to:  
   **Settings** → **Data Inputs** → **TCP** → **New Local TCP**  
3. **Port**: Set to `9000` (or another port).  
4. **Source Type**:  
   - Choose **Operating System** → `linux_secure`.  
5. **Host**: Choose **IP** and enter your Linux machine’s IP.  
6. **Save and Submit**.  

---



### 6. Allow Outgoing Traffic from Linux Machine (Optional)  
If your Linux machine has a firewall, allow outgoing traffic:  
```bash
sudo ufw allow out to <splunk-server-ip> port 9000 proto tcp
sudo ufw reload
```

---


### 8. Run the Scripts  

- **Run all scripts at once**:  
   ```bash
   sudo python3 main.py
   ```  
- **Run individually**:  
   ```bash
   sudo python3 application_log.py
   sudo python3 security_log.py
   sudo python3 system_log.py
   ```  





