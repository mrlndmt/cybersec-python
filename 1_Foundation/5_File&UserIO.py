# File - User I/O
# -------------
# READING a user input
target = input("Enter target IP: ")
print(f"Scanning {target}...")

# 'input()' always stores whatever the user types as STRING.
# So if you need a number (int), cast it:
port = input("Enter port: ")         # "80" — still a string
port = int(port)                     # 80 — now an integer

port = int(input("Enter port: "))    # same in one line
print(f"Port input is directly set as a {type(port)}")

# ---------
# READING a file - wordlist attack example
with open("password.txt", "r") as f:    # "r" is the READING MODE, it tells Python how you want to open the file
    for line in f:
        password = line.strip()         # remove newline character
        print(f"Trying: {password}")

# Read all lines into a list at once
with open("targets.txt", "r") as f:
    targets = [line.strip() for line in f if line.strip()]

# ---------
# Read a file that might not exist - safe version
import os
filename = "targets.txt"
if os.path.exists(filename):
    with open(filename, "r") as f:
        data = f.read()
else:
    print(f"File not found: {filename}")

# Hardcoding a path might be fragile. Sometimes it is required to accept it as input:
import os
wordlist_path = input("Enter wordlist path: ").strip()
if not os.path.exists(wordlist_path):
    print(f"[-] File not found: {wordlist_path}")
else:
    with open(wordlist_path, "r", errors="ignore") as f:
        words = [line.strip() for line in f]

# ---------
# WRITTING results to a file
open_ports = [22, 80, 443]
with open("results.txt", "w") as f:     # "w" = overwrite
    for port in open_ports:
        f.write(f"OPEN: {port}")

# ---------
# APPENDING - don't overwrite, add to the end
with open("results.txt", "a") as f:     # "a" = append
    f.write("Scan complete.")

# ---------
# Practical: load a wordlist, skip blank lines and comments
def load_wordlist(path):
    with open(path, "r", errors="ignore") as f:
        return [l.strip() for l in f if l.strip() and not l.startswith("#")]

# -----------------
# Exercise: Write a function `save_results(filename, results)` that takes a filename and a list of strings, and saves each string on its own line. 
# Then write a function `load_targets(filename)` that reads a file and returns a clean list (no blank lines, no whitespace). Test both.
def save_results(filename, results):
    with open(filename, "w") as f:
        for r in results:
            f.write(r + "\n")

def load_targets(filename):
    with open(filename, "r") as f:
        return [l.strip() for l in f if l.strip()]

save_results("out.txt", ["10.0.0.1:80 OPEN", "10.0.0.2:22 OPEN"])
print(load_targets("out.txt"))
