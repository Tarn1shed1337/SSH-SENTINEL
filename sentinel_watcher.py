import re 
import subprocess
import time
from sentinel_logger import log_event

LOG_FILE = "/var/log/auth.log"

MAX_ATTEMPTS = 5
BAN_CMD = ["sudo","iptables","-A","INPUT","-s","{IP}" ,"-j","DROP"]

def ban_ip(ip):
    tool = "ip6tables" if ":" in ip else "iptables"
    print(f"Banning {ip} (Attempts threshold reached)")
    cmd = [tool, "-A", "INPUT", "-s", ip, "-j", "DROP"]
    try:
        subprocess.run(cmd , check=True)
        print(f"Firewall updated : {ip} is now blocked.")
        log_event(ip ,"Banned" , "Maximum attempts reached")
    except subprocess.CalledProcessError:
        print(f"Failed to block the IP addr : {ip}")

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
                    print("Found a 'Failed password' line in the log!")
                    match = re.search(r"from\s+(\S+)", line)
                    if match:
                        ip = match.group(1)
                        print(f"Regex matched! Extracted IP: {ip}")
                        failed_attempts[ip] = failed_attempts.get(ip,0) + 1
                        print(f"Current count for {ip}: {failed_attempts[ip]}/{MAX_ATTEMPTS}")
                        if failed_attempts[ip] >= MAX_ATTEMPTS:
                            print(f"Threshold reached. Calling ban_ip({ip})...")
                            ban_ip(ip)
                            failed_attempts[ip] = -1000 # this is just a de-duplication
                    else:
                        print("Regex did not match.")


    except KeyboardInterrupt:
        print("\n Watcher stopped by user.")
    except FileNotFoundError:
        print(f"Error: {LOG_FILE} not found")

if __name__ == "__main__":
    watch_logs()

