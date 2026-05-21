# --- Phase 3 Project : Multithreaded port scanner ---
# ----------------------------------------------------
# Build a fast multithreaded port scanner with web fingerprinting that saves a full JSON report.

import os
import sys
import argparse
import re
import json
import socket
from datetime import datetime
import time
import threading
import requests
from urllib.parse import urlparse, urlencode, quote, urljoin
#from scapy.all import IP, TCP, sr1, sniff

# What should it do:
# 1. Accept a target via argparse (-t)
# 2. Accept a port range (-s start, -e end, defaults 1-1024)
# 3. Validate the IP/hostname
# 4. Resolve hostname to IP once
# 5. Scan all ports in range using threads + semaphore
# 6. For any open port, attempt banner grab
# 7. If port 80 is open, run fingerprint()
# 8. Save full JSON report (-o flag)
# 9. Log everything with timestamps (-v for verbose)

# --- logs ---
def log(msg, level="*"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [{level}] {msg}")

# --- validate target IP ---
def valid_target(target):
    # accept IPs
    if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", target):
        log("IP is valid", "+")
        return True
    # accept hostnames like scanme.nmap.org
    if re.match(r"^[a-zA-Z0-9][a-zA-Z0-9\.\-]+$", target):
        log("Hostname is valid", "+")
        return True
    log("Invalid target", "-")
    return False

# --- threaded port scan ---
open_ports = []
lock = threading.Lock()
sem = threading.Semaphore(100)
scanned = 0
scanned_lock = threading.Lock()

def scan_port(ip, port, total):
    global scanned
    with sem:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        if sock.connect_ex((ip, port)) == 0:
            with lock:
                open_ports.append(port)
                print(f"\r[+] Port {port} open" + " " * 20)
        sock.close()
        with scanned_lock:
            scanned += 1
            print(f"\r[*] Progress: {scanned}/{total}", end="", flush=True)

# --- scan port range ---
def scan_range(ip, start, end):
    ip = socket.gethostbyname(ip)
    total = end - start + 1
    threads = []
    for port in range(start, end + 1):
        t = threading.Thread(target=scan_port, args=(ip, port, total))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    print()
    return ip, sorted(open_ports)

# --- grab banner ---
def grab_banner(ip, port):
    try:
        sock = socket.socket()
        sock.settimeout(2)
        sock.connect((ip, port))
        raw = sock.recv(1024)
        banner = raw.decode("utf-8", errors="ignore").strip()
        return banner
    except Exception as e:
        log(f"Connection to {ip} Failed: {e}", "-")
        return None
    finally:
        sock.close()

# --- url fingerprinting ---
def fingerprint(url):
    try:
        r = requests.get(url, timeout=3)
        fingerprint = {
            "status":     r.status_code,
            "server":     r.headers.get("Server", "not found"),
            "powered_by": r.headers.get("X-Powered-By", "not found"),
            "login_form": "password" in r.text.lower()
        }
        log(f"Fingerprint succeed: {url}", "+")

        if fingerprint["login_form"]:
            log("Login form detected", "+")
        else:
            log("No login form found", "-")
        
        return fingerprint
    
    except requests.exceptions.RequestException as e:
        log(f"Fingerprint failed: {e}", "-")
        return {}

# --- save report ---
def save_output(report, ip, now):
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    filename = f"recon_{ip}_{timestamp}.json"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, filename)
    with open(output_path, "w") as f:
        json.dump(report, f, indent=4)
    log(f"Report saved: {output_path}", "+")

# --- argparse layer ---
scanner = argparse.ArgumentParser(description="Port Scanner")
scanner.add_argument("-t",  "--target",     required=True,          help="Target IP")
scanner.add_argument("-s",  "--start",      type=int, default=1,    help="Port range's start (default: 1)")
scanner.add_argument("-e",  "--end",        type=int, default=1024, help="Port range's end (default: 1024)")
scanner.add_argument("-o",  "--output",     action="store_true",    help="Save results to JSON file")
scanner.add_argument("-v",  "--verbose",    action="store_true",    help="Verbose mode")
args = scanner.parse_args()

# --- execution layer ---
now = datetime.now()
timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
start = args.start
end = args.end

if not valid_target(args.target):
    sys.exit(1)

if args.verbose:
    log(f"Starting scan on {args.target}:{start}-{end}...")
    time.sleep(1)

ip, ports = scan_range(args.target, start, end)

banners = {}
for p in ports:
    if p == 80:
        continue
    banner = grab_banner(ip, p)
    if banner:
        banners[p] = banner         

http_data = {}
if 80 in ports:
    url = f"http://{args.target}"
    http_data = fingerprint(url)
    
report = {
    "target":     args.target,
    "ip":         ip,
    "timestamp":  timestamp,
    "open_ports": ports,
    "banners":    banners,
    "http":       http_data
}

if args.output:
    save_output(report, args.target, now)