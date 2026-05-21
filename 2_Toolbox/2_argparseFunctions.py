# argparse - each argument is wired to functions to actually work
# -----------------------
import argparse
import socket
import os

# --- The actual work functions ---

def scan_port(ip, port, timeout=1):
    try:
        sock = socket.socket()
        sock.settimeout(timeout)
        sock.connect((ip, port))
        sock.close()
        return True
    except:
        return False

def save_result(filepath, line):
    with open(filepath, "a") as f:
        f.write(line + "\n")

# --- The argument layer ---

parser = argparse.ArgumentParser(description="Simple port scanner")
parser.add_argument("-t", "--target",  required=True,           help="Target IP address")
parser.add_argument("-p", "--port",    type=int, default=80,    help="Port to scan (default: 80)")
parser.add_argument("-v", "--verbose", action="store_true",     help="Enable verbose output")
parser.add_argument("-o", "--output",                           help="Save results to this file")
args = parser.parse_args()

# --- Wire arguments to the functions ---

if args.verbose:
    print(f"[*] Starting scan on {args.target}:{args.port}")

is_open = scan_port(args.target, args.port)

if is_open:
    result = f"[OPEN]   {args.target}:{args.port}"
else:
    result = f"[CLOSED] {args.target}:{args.port}"

print(result)

if args.output:
    save_result(args.output, result)
    if args.verbose:
        print(f"[*] Result saved to {args.output}")
