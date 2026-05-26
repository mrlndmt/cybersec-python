# --- Phase 4 Project : Toolkit ---
# ---------------------------------
# Build a full recon toolkit using previous functionalities and add enumeration

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
# 1. Validate target (IP or hostname)
# 2. Multithreaded port scan with progress counter
# 3. Banner grab on open ports
# 4. HTTP fingerprint if port 80 found
# 5. Subdomain enumeration (if target is a hostname)
# 6. Web directory fuzzing (if port 80 found)
# 7. Save full JSON report with all findings

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

# --- subdomain enumeration ---
found_subs = []
sub_lock = threading.Lock()
sub_sem = threading.Semaphore(50)

def check_subdomain(domain, sub):
    with sub_sem:
        hostname = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(hostname)
            with sub_lock:
                found_subs.append((hostname, ip))
                print(f"[+] {hostname} -> {ip}")
        except socket.gaierror:
            pass

def enumerate_subdomain(domain, wordlist):
    log(f"Enumerating subdomains for {domain}")
    threads = []
    for sub in wordlist:
        t = threading.Thread(target=check_subdomain, args=(domain, sub))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    return found_subs

# --- web directory fuzzing ---
found_directories = []
fuzz_lock = threading.Lock()
fuzz_sem = threading.Semaphore(20)

def check_path(base_url, path):
    with fuzz_sem:
        url = f"{base_url}/{path}"
        try:
            r = requests.get(url, timeout=3, allow_redirects=False)
            if r.status_code not in [404, 400]:
                with fuzz_lock:
                    found_directories.append((path, r.status_code))
                    log(f"{r.status_code} - {url}", "+")
        except requests.exceptions.RequestException:
            pass

def fuzz(base_url, wordlist_path):
    with open(wordlist_path, "r", errors="ignore") as f:
        paths = []
        for line in f:
            line = line.strip()
            if line:
                paths.append(line)    
    
    log(f"Fuzzing {base_url} with {len(paths)} paths")
    threads = []
    for path in paths:
        t = threading.Thread(target=check_path, args=(base_url, path))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    return found_directories

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
scanner.add_argument("-w",  "--wordlist",                           help="Wordlist path for directory fuzzing")
args = scanner.parse_args()

# -----------------------
# --- EXECUTION LAYER ---
# -----------------------
now = datetime.now()
timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
start = args.start
end = args.end

common_directories = ["admin", "login", "dashboard", "config", "backup",
          "robots.txt", ".git", "api", "uploads", "phpmyadmin"]

common_subs = [
    "www", "mail", "ftp", "dev", "staging", "admin",
    "api", "vpn", "remote", "portal", "blog", "shop",
    "test", "beta", "cdn", "static", "assets", "ns1", "ns2"]

# --- validate IP ---
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

# --- http fingerprint if port 80 found ---
http_data = {}
dirs = []
subs = []

# --- JSON report ---
report = {
    "target":       args.target,
    "ip":           ip,
    "timestamp":    timestamp,
    "open_ports":   ports,
    "banners":      banners,
    "http":         http_data,
    "subdomains":   subs,
    "directories":  dirs
}

if 80 in ports:
    url = f"http://{args.target}"
    http_data = fingerprint(url)
    if args.wordlist:
        dirs = fuzz(url, args.wordlist)       # file wordlist
    else:
        for path in common_directories:
            check_path(url, path)             # fallback to built-in list
        dirs = found_directories
    report["directories"] = dirs

# --- subdomain enumeration if it's a hostname ---
is_hostname = not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", args.target)

if is_hostname:
    subs = enumerate_subdomain(args.target, common_subs)
    report["subdomains"] = subs

if args.output:
    save_output(report, args.target, now)