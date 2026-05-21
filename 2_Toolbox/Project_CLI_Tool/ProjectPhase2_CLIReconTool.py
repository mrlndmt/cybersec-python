# --- Phase 2 Project : CLI Reconnaissance Tool ---
# -------------------------------------------------
# Give it a target IP, it pings it, grabs the SSH banner, 
# saves a timestamped JSON report, and logs everything to the terminal.
# -------------------------------------------------
# Typical structure of a code:
# 1. 'imports'          = everything else depends on these, so always first
# 2. 'definitions'      = your functions live here, defined before they're used
# 3. 'configuration'    = argparse goes here, collecting what the user wants
# 4. 'execution'        = the actual work happens here, using the functions and args above
# /!\ Nothing should reference something defined below it. /!\
# -------------------------------------------------
import os
import sys
import argparse
import re
import subprocess
import json
import socket
from datetime import datetime
import time

# --- logs ---
def log(msg, level="*"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [{level}] {msg}")

# --- validate the IP ---
def ip_format(ip):
    match = re.search(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip)
    if not match:
        log("Invalid IP address", "-")
        return False
    return True

# --- ping command ---
def ping_host(ip):
    flag = "-n" if sys.platform == "win32" else "-c"
    result = subprocess.run(
        ["ping", flag, "1", ip],
        capture_output=True,
        text=True
    )
    return result.returncode == 0

# --- banner grabbing ---
def grab_banner(ip, port):
    try:
        sock = socket.socket()
        sock.connect((ip, port))
        raw = sock.recv(1024)
        banner = raw.decode("utf-8", errors="ignore").strip()
        log(f"Port {port} open", "+")
        time.sleep(1)
        return banner
    except Exception as e:
        log(f"Connection to {ip} Failed: {e}", "-")
        return None
    finally:
        sock.close()

# --- save the output + timestamp ---
def save_output(result, ip, now):
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    filename = f"recon_{ip}_{timestamp}.json"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, filename)
    with open(output_path, "w") as f:
        json.dump(result, f, indent=4)
    log(f"Report saved: {output_path}", "+")

# --- arguments layer ---
pinger = argparse.ArgumentParser(description="Ping tool")
pinger.add_argument("-t", "--target",   required=True,          help="Target IP")
pinger.add_argument("-p", "--port",     type=int, default=80,   help="Port to scan (default: 80)")
pinger.add_argument("-v", "--verbose",  action="store_true",    help="Verbose output")
pinger.add_argument("-o", "--output",   action="store_true",    help="Save results to file")
args = pinger.parse_args()

# --- execution layer ---
now = datetime.now()
timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
ip = args.target
port = args.port

if not ip_format(ip):
    sys.exit(1)

if args.verbose:
    log(f"Starting scan on {ip}:{port}...")
    time.sleep(1)

host_up = ping_host(ip)
if host_up:
    log("Host is up", "+")
else:
    log(f"{ip} did not respond", "-")

banner = grab_banner(ip, port)

result = {
    "target":       ip,
    "timestamp":    timestamp,
    "host_up":      host_up,
    "port":         port,
    "banner":       banner if host_up else None
}

if args.output:
    save_output(result, ip, now)

print(f"\n--- Scan results ---\n-Timestamp: {timestamp}\n-Target: {ip}\n-Port: {port}\n-Host up: {host_up}\n-Banner: {banner}\n")
