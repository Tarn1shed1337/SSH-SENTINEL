# SSH Sentinel: Automated Hardening & Intrusion Prevention
### **Developed by Med Chemseddin Boufaris**
**SSH Sentinel** is a lightweight, Python-based security suite designed to audit Linux system configurations and provide active defense against brute-force attacks. It combines a system hardener with a real-time log watcher to detect and block malicious actors using `iptables` and `ip6tables`.

#
---

## 🚀 Features

*   **System Audit & Hardening:** Scans `sshd_config` for security vulnerabilities and applies industry-standard fixes automatically.
*   **Real-time Monitoring:** Watches `/var/log/auth.log` for failed authentication attempts.
*   **Dual-Stack Protection:** Supports both **IPv4** and **IPv6** (including `::1` localhost testing) banning logic.
*   **Intelligent Banning:** Automatically triggers firewall drops after a configurable threshold (Default: **5 attempts**).
*   **Professional Logging:** Records every security event, audit, and ban in a structured `sentinel_events.csv` for forensic analysis.

---

## 📂 Project Structure

| File | Description |
| :--- | :--- |
| `main.py` | The central orchestrator and menu system. |
| `sentinel_hardener.py` | Logic for auditing and modifying SSH configurations. |
| `sentinel_watcher.py` | The IPS engine that monitors logs and triggers bans. |
| `sentinel_logger.py` | Modular logging system for CSV event recording. |
| `requirements.txt` | List of Python dependencies. |

---

## 🛠️ Installation & Setup

### 1. Prerequisites
Ensure you are running on a Linux distribution (optimized for **Kali Linux** or **Debian**). 

### 2. Install Dependencies
To keep the system clean and ensure the Root user has access to the UI components, install `pyfiglet` via the system package manager:
```bash
sudo apt update && sudo apt install python3-pyfiglet -y 
```
### 3. Clone repository
```bash
git clone [https://github.com/Tarn1shed1337/SSH-Sentinel.git](https://github.com/Tarn1shed1337/SSH-Sentinel.git)
cd SSH-Sentinel
```
### Usage
Because this tool modifies system firewall rules and reads protected log files, it must be run with root privileges.

```bash
sudo python3 main.py
```
Operating Modes:
<ol>
<li>Audit & Harden: Scans your SSH configuration for weaknesses and offers to fix them.</li>

<li>Start Watcher: Initiates the real-time IPS to monitor failures and update your firewall.</li>

<li>Exit: Gracefully closes the suite.</li>
</ol>
