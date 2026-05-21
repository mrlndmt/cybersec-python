# os & sys
# -------------
import os
import sys

# --- os: interact with the filesystem and evironment ---

# Get current working directory
print(os.getcwd())

# Build paths safely (works on Linus AND Windows)
wordlist = os.path.join("/usr", "share", "wordlists", "rockyou.txt")
print(wordlist)

# Check if a file or folder exists before touching it
if os.path.exists(wordlist):
    print("[+] Wordlist found")
else:
    print("[-] Wordlist not found")

os.path.isfile("scan.py")           # True if it's a file
os.path.isdir("/tmp/results")       # True if it's a folder

# os.path.join() - right way to build file paths
base    = "/home/user/pentests"
target  = "10.0.0.1"
date    = "15-01-2024"

output_dir = os.path.join(base, target, date)
print(output_dir)

report = os.path.join(output_dir, "scan_results.json")
print(report)

# Create a folder (safe version - no crash if it already exists)
os.makedirs("/tmp/results", exist_ok=True)

# List files in a directory
for f in os.listdir("/tmp/results"):
    print(f)

# Get environment variables - useful for API keys, config
home = os.environ.get("HOME", "/tmp")       # default if not set
print(home)

# --- sys: interact with the Python runtime itself ---

# sys.argv - command line arguments passed to your script
# If you run: python3 scanner.py 192.168.1.1 80
print(sys.argv)                     # ['scanner.py', '192.168.1.1', '80']
print(sys.argv[0])                  # 'scanner.py'  (the script name)
#print(sys.argv[1])                  # '192.168.1.1' (first argument)

# Exit the script early with an error message
if len(sys.argv) < 2:
    print("Usage: scanner.py ")
    sys.exit(1)                     # exit code 1 = error

# -----------------
# Exercises: Write a script that: 
# (1) creates a folder called 'output' in the current directory if it doesn't exist, 
# (2) checks if a file called 'targets.txt' exists in the current directory and prints whether it was found or not, 
# (3) prints all files currently in the 'output' folder.
import os

os.makedirs("output", exist_ok=True)
print("[+] output/ folder ready")

if os.path.exists("target.txt"):
    print("[+] target.txt found")
else:
    print("[-] target.txt not found")

files = os.listdir("output")
if files:
    for f in files:
        print(f" {f}")
else:
    print(" (empty)")
