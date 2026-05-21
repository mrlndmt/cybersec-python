# port scanner - with progress counter
# --------------

import socket, threading, argparse, json, sys
from datetime import datetime

# Phase 3 mini-project with one upgrade:
# a progress counter so you know the scan is still running.

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
            # overwrite current line with progress
            print(f"\r[*] Progress: {scanned}/{total}", end="", flush=True)

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
    print()         # new line after progress line
    return ip, sorted(open_ports)

# print(f"\r[*] Progress: {n}/{total}", end="", flush=True)
# \r (carriage return)  = moves cursor back to start of current line without newline,
#                         lets you overwrite the same line repeatedly — progress bar effect
# end=""                = don't print a newline
# flush=True            = force output immediately (no buffering)

# [i] The `\r` trick is used in almost every real CLI tool to show live progress 
# without flooding the terminal with lines. Learn it once, use it everywhere.

# ---------------
# Exercise: Add the progress counter to your Phase 3 port scanner. 
# Run it against scanme.nmap.org ports 1-1024 and watch the counter tick up in real time. 
# Notice how much faster it feels with visual feedback.