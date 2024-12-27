# Splunk Log Forwarding - Overview  

This repository contains Python scripts for forwarding system logs (Application, Security, and System) from both **Windows** and **Linux** machines to a Splunk server over TCP.  

## 📂 Project Structure  
```
/  
│  
├── Linux_version/  
│   ├── application_log.py  
│   ├── security_log.py  
│   ├── system_log.py
│   ├── README.md  
│   └── main.py  
│  
├── Windows_version/  
│   ├── application_log.py  
│   ├── security_log.py  
│   ├── system_log.py
│   ├── README.md
│   └── main.py  
│  
└── README.md  
```  

## How It Works  
- **Windows Logs** – Collected using `win32evtlog` to extract Event Viewer logs.  
- **Linux Logs** – Logs are retrieved using `journalctl` and `dmesg` commands.  
- **Log Upload** – Logs are sent to Splunk over TCP in JSON format.  
- **Automation** – The `main.py` script in both folders triggers all log scripts at once.  

## 🛠️ Setup  
- **Windows** – Requires Python 3, `pywin32`, and Administrator privileges.  
- **Linux** – Requires Python 3, `journalctl`, and `dmesg`.  

## 📘 Instructions  
- Follow the platform-specific README files in the `windows` and `linux` folders for installation and setup.  
- Update Splunk server IP and port in each script before running.  

---

Contributions and suggestions are welcome! 🚧