import subprocess

def run_scripts():
    scripts = ["application_log.py", "security_log.py", "system_log.py"]
    
    for script in scripts:
        subprocess.run(["python3", script])

if __name__ == "__main__":
    run_scripts()
