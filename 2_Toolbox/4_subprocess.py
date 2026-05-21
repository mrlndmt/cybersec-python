# subprocess - run system commands and capture their output
# ---------------
import subprocess

# subprocess lets you run shell commands from inside Python
# This is how you integrate nmpa, netcat, curl, etc.

# Run a command and capture output
result = subprocess.run(
    ["ping", "-n", "1", "8.8.8.8"],        # full command as a list; flag '-n' for Windows, '-c' for Linux
    capture_output = True,                 # grab stdout and folder
    text = True                            # return strings, not byte
)

print(result.stdout)                       # the output of the command
print(result.returncode)                   # 0 = success, anything else = error

# Check if the command succeeded
if result.returncode == 0:
    print("[+] Host is up")
else:
    print("[-] Host is down or unreachable")

# Run nmap and capture results
def run_nmap(target, ports="1-1024"):
    result = subprocess.run(
        ["nmap", "-p", ports, target],
        capture_output = True,
        text = True
    )
    return result.stdout

#output = run_nmap("scanme.nmap.org")
#print(output)

# Check if a tool is installed before using it
def tool_exists(tool_name):
    result = subprocess.run(
        ["which", tool_name],
        capture_output = True,
        text = True
    )
    return result.returncode == 0

if tool_exists("nmap"):
    print("[+] nmap is available")
else:
    print("[-] nmap not found — install with: apt install nmap")

# --- /!\ IMPORTANT /!\ --- 
# Always pass commands as a LIST ['nmap', '-p', '80'] and NOT as a STRING 'nmap -p 80'. 
# The list form is safer (no shell injection risk) and works more reliably across systems.

# -------------------
# Exercise: Write a function called `ping_host(ip)` that runs `ping -c 1 ` using subprocess, 
# checks the return code, and returns True if the host responded or False if not. 
# Then loop through ['8.8.8.8', '1.1.1.1', '192.168.99.99'] and print which are up or down.
def ping_host(ip):
    result = subprocess.run(
        ["ping", "-n", "1", ip],        # flag '-n' for Windows, '-c' for Linux
        capture_output = True,
        text = True
    )
    return result.returncode == 0

targets = ['8.8.8.8', '1.1.1.1', '192.168.99.99']
for ip in targets:
    if ping_host(ip):
        print(f"Host {ip} is UP")
    else:
        print(f"Host {ip} is DOWN")

# -------------------
# --- Other clean way that handles both Windows and Linux ---
import subprocess
import sys

def ping_host(ip):
    # Pick the right flag depending on the OS
    flag = "-n" if sys.platform == "win32" else "-c"
    result = subprocess.run(
        ["ping", flag, "1", ip],
        capture_output=True,
        text=True
    )
    return result.returncode == 0

targets = ["8.8.8.8", "1.1.1.1", "192.168.99.99"]
for ip in targets:
    status = "UP" if ping_host(ip) else "DOWN"
    print(f"{ip} — {status}")
