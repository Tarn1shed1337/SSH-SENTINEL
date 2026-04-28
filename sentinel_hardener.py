# Created By Tarnished / Chemseddin

import re
import shutil
import subprocess

CONFIG_FILE_PATH = "sshd_config_practice" # this is my practice file directory u can change it to yours

POLICY = {
    "PORT" : "2222",
    "PasswordAuthentication" : "no",
    "PermitRootLogin": "no"
    # you can add more policies
}

def run_audit():
    print(f"Analyzing {CONFIG_FILE_PATH} ... \n")

    found_settings = {}
    try:
        with open(CONFIG_FILE_PATH,"r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") :
                    continue
                
                for setting in POLICY:
                    pattern = rf"^{setting}\s+(.*)"

                    match = re.search(pattern , line , re.IGNORECASE)
                    if match :
                        found_settings[setting] = match.group(1).strip()                    
        for setting, safe_value in POLICY.items():
             if setting in found_settings:
                current_val = found_settings[setting]
                if current_val == safe_value:
                    print(f"The setting {setting} is already set to {current_val}")
                else:
                    print(f"The setting {setting} is set to {current_val} but should be {safe_value}")
             else:
                print(f"The setting {setting} is not found in the config file, it should be set to {safe_value}")
        return True
    except FileNotFoundError:
        print(f"Error: The file {CONFIG_FILE_PATH} was not found.")
        return False
def apply_fixes():
    shutil.copy(CONFIG_FILE_PATH, CONFIG_FILE_PATH + ".bak")

    new_config_lines = []

    with open(CONFIG_FILE_PATH, "r") as f:
        lines = f.readlines()
    fixed_settings = set()

    for line in lines :
        modified = False

        for setting , safe_value in POLICY.items():
            pattern = rf"^{setting}\s+(.*)"
            if re.search(pattern, line ,re.IGNORECASE):
                new_config_lines.append(f"{setting} {safe_value}\n")
                fixed_settings.add(setting)
                modified = True
                break
        
        if not modified:
            new_config_lines.append(line)

    for setting , safe_value in POLICY.items():
        if setting not in fixed_settings:
            new_config_lines.append(f"{setting} {safe_value} \n")
            print(f"Added missing setting : {setting}")
    with open(CONFIG_FILE_PATH,"w") as f:
        f.writelines(new_config_lines)
    
    print("Fixes Applied (File Updated)")
    restart_ssh()

def restart_ssh():
    print("Restarting SSH service to apply changes ...")
    try:
        subprocess.run(['sudo' , 'systemctl' , 'restart' , 'ssh'])
        print("SSH service restarted successfully.")
    except subprocess.CalledProcessError:
        print("Error: Failed to restart SSH service.")

