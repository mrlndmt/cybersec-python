# --- Phase 4 Project : Toolkit ---
# ---------------------------------
# Build a full recon toolkit using previous functionalities and add enumeration

import os
import sys
import argparse
import re
import json
import socket
import time
import threading
import requests
from datetime import datetime

# What should it do:
# 1. Validate target (IP or hostname)
# 2. Multithreaded port scan with progress counter
# 3. Banner grab on open ports
# 4. HTTP fingerprint if port 80 found
# 5. Subdomain enumeration (if target is a hostname)
# 6. Web directory fuzzing (if port 80 found)
# 7. Save full JSON report with all findings

# ----------------------------------------------
#  HELPERS
# ----------------------------------------------

def log(msg, level="*"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [{level}] {msg}")

def valid_target(target):
    if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", target):
        log("IP is valid", "+")
        return True
    if re.match(r"^[a-zA-Z0-9][a-zA-Z0-9\.\-]+$", target):
        log("Hostname is valid", "+")
        return True
    log("Invalid target", "-")
    return False

def is_hostname(target):
    return not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", target)

# ----------------------------------------------
#  PORT SCANNING
# ----------------------------------------------

open_ports   = []
lock         = threading.Lock()
sem          = threading.Semaphore(100)
scanned      = 0
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

def scan_range(target, start, end):
    ip    = socket.gethostbyname(target)
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

# ----------------------------------------------
#  BANNER GRABBING
# ----------------------------------------------

def grab_banner(ip, port):
    try:
        sock = socket.socket()
        sock.settimeout(2)
        sock.connect((ip, port))
        raw    = sock.recv(1024)
        banner = raw.decode("utf-8", errors="ignore").strip()
        return banner
    except Exception as e:
        log(f"Banner grab failed on {ip}:{port} — {e}", "-")
        return None
    finally:
        sock.close()

# ----------------------------------------------
#  HTTP FINGERPRINTING
# ----------------------------------------------

def fingerprint(url):
    try:
        r      = requests.get(url, timeout=3)
        result = {
            "status":     r.status_code,
            "server":     r.headers.get("Server",       "not found"),
            "powered_by": r.headers.get("X-Powered-By", "not found"),
            "login_form": "password" in r.text.lower()
        }
        log(f"Fingerprint OK: {url}", "+")
        log("Login form detected" if result["login_form"] else "No login form", "+" if result["login_form"] else "-")
        return result
    except requests.exceptions.RequestException as e:
        log(f"Fingerprint failed: {e}", "-")
        return {}

# ----------------------------------------------
#  DIRECTORY FUZZING
# ----------------------------------------------

found_directories = []
fuzz_lock         = threading.Lock()
fuzz_sem          = threading.Semaphore(20)

def check_path(base_url, path):
    with fuzz_sem:
        url = f"{base_url}/{path.lstrip('/')}"
        try:
            r = requests.get(url, timeout=3, allow_redirects=False)
            if r.status_code not in [404, 400]:
                with fuzz_lock:
                    found_directories.append((path, r.status_code))
                    log(f"{r.status_code} — {url}", "+")
        except requests.exceptions.RequestException:
            pass

def fuzz(base_url, wordlist_path):
    try:
        with open(wordlist_path, "r", errors="ignore") as f:
            paths = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        log(f"Wordlist not found: {wordlist_path}", "!")
        return []
    log(f"Fuzzing {base_url} with {len(paths)} paths")
    threads = [threading.Thread(target=check_path, args=(base_url, path)) for path in paths]
    for t in threads: t.start()
    for t in threads: t.join()
    return found_directories

# ----------------------------------------------
#  SUBDOMAIN ENUMERATION
# ----------------------------------------------

found_subs = []
sub_lock   = threading.Lock()
sub_sem    = threading.Semaphore(50)

def check_subdomain(domain, sub):
    with sub_sem:
        hostname = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(hostname)
            with sub_lock:
                found_subs.append((hostname, ip))
                log(f"{hostname} -> {ip}", "+")
        except socket.gaierror:
            pass

def enumerate_subdomains(domain, wordlist):
    log(f"Enumerating subdomains for {domain}")
    threads = [threading.Thread(target=check_subdomain, args=(domain, sub)) for sub in wordlist]
    for t in threads: t.start()
    for t in threads: t.join()
    return found_subs

# ----------------------------------------------
#  REPORT
# ----------------------------------------------

def save_output(report, target, now):
    timestamp   = now.strftime("%Y%m%d_%H%M%S")
    filename    = f"recon_{target}_{timestamp}.json"
    script_dir  = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, filename)
    with open(output_path, "w") as f:
        json.dump(report, f, indent=4)
    log(f"Report saved: {output_path}", "+")

# ----------------------------------------------
#  ARGPARSE
# ----------------------------------------------═

scanner = argparse.ArgumentParser(description="Recon & enumeration toolkit")
scanner.add_argument("-t", "--target",   required=True,          help="Target IP or hostname")
scanner.add_argument("-s", "--start",    type=int, default=1,    help="Port range start (default: 1)")
scanner.add_argument("-e", "--end",      type=int, default=1024, help="Port range end (default: 1024)")
scanner.add_argument("-w", "--wordlist",                         help="Wordlist path for directory fuzzing")
scanner.add_argument("-o", "--output",   action="store_true",    help="Save results to JSON file")
scanner.add_argument("-v", "--verbose",  action="store_true",    help="Verbose output")
args = scanner.parse_args()

# ----------------------------------------------
#  EXECUTION
# ----------------------------------------------

now       = datetime.now()
timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

common_directories = [
    "admin", "login", "dashboard", "config", "backup",
    "robots.txt", ".git", "api", "uploads", "phpmyadmin"
]
common_subs = [
    "www", "mail", "ftp", "dev", "staging", "admin",
    "api", "vpn", "remote", "portal", "blog", "shop",
    "test", "beta", "cdn", "static", "assets", "ns1", "ns2"
]

# 1. validate
if not valid_target(args.target):
    sys.exit(1)

if args.verbose:
    log(f"Starting scan on {args.target} ports {args.start}-{args.end}")
    time.sleep(1)

# 2. port scan
ip, ports = scan_range(args.target, args.start, args.end)
log(f"Found {len(ports)} open port(s): {ports}")

# 3. banner grab
banners = {}
for p in ports:
    if p == 80:
        continue
    banner = grab_banner(ip, p)
    if banner:
        banners[p] = banner

# 4. http fingerprint + directory fuzzing
http_data = {}
dirs      = []
if 80 in ports:
    url       = f"http://{args.target}"
    http_data = fingerprint(url)
    if args.wordlist:
        dirs = fuzz(url, args.wordlist)
    else:
        for path in common_directories:
            check_path(url, path)
        dirs = found_directories

# 5. subdomain enumeration
subs = []
if is_hostname(args.target):
    subs = enumerate_subdomains(args.target, common_subs)

# 6. build report
report = {
    "target":      args.target,
    "ip":          ip,
    "timestamp":   timestamp,
    "open_ports":  ports,
    "banners":     banners,
    "http":        http_data,
    "directories": dirs,
    "subdomains":  subs
}

# 7. save
if args.output:
    save_output(report, args.target, now)