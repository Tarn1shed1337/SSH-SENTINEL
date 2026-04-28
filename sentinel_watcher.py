import re 
import subprocess
import time

LOG_FILE = "/var/log/auth.log"
MAX_ATTEMPTS = 5
BAN_CMD = ["sudo","iptables","-A","INPUT","-s","{IP}" ,"-j","DROP"]

def ban_ip(ip):
    print(f"Banning {ip} (Attempts threshold reached)")
    current_ban_cmd = [arg.replace("{IP}",ip) for arg in BAN_CMD]
    try:
        subprocess.run(current_ban_cmd , check=True)
        print(f"Firewall updated : {ip} is now blocked.")
    except subprocess.CalledProcessError:
        print("Failed to block the IP addr : {ip}")

def watch_logs():
    print(f"Sentinel Watcher is active and Monitoring {LOG_FILE} ...")
    failed_attempts= {}
    try:
        with open(LOG_FILE,"r") as f:
            f.seek(0,2)
            while True:
                line = f.readline()
                if not line:
                    time.sleep(0.1)
                    continue
                if "Failed password" in line:
                    match = re.search(r"from\s+(\d{1,3}(?:\.\d{1,3}){3})", line)
                    if match:
                        ip = match.group(1)
                        failed_attempts[ip] = failed_attempts.get(ip,0) + 1
                        if failed_attempts[ip] >= MAX_ATTEMPTS:
                            ban_ip(ip)
                            failed_attempts[ip] = -1000 # this is just a de-duplication
    except KeyboardInterrupt:
        print("\n Watcher stopped by user.")
    except FileNotFoundError:
        print(f"Error: {LOG_FILE} not found")

if __name__ == "__main__":
    watch_logs()

