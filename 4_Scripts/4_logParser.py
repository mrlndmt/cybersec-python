# log parser - extrat IP, errors, anomalies from log files
# ------------
import re
from collections import Counter

# log files contain a wealth of intel:
# failed logins, port scans, error patterns, active IPs

sample_log = """
Jan 15 03:21:01 server sshd: Failed password for root from 10.0.0.5 port 22
Jan 15 03:21:02 server sshd: Failed password for root from 10.0.0.5 port 22
Jan 15 03:21:03 server sshd: Failed password for admin from 10.0.0.99 port 22
Jan 15 03:21:05 server sshd: Accepted password for deploy from 10.0.0.1 port 22
Jan 15 03:22:00 server sshd: Failed password for root from 10.0.0.5 port 22
"""

# --- extract all IPs ---
ips = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", sample_log)
# set() is a Python data type that holds only unique values; it automatically removes duplicates
print("All IPs:", set(ips))

# while list() would display everything, even duplicates
print("All IPs:", list(ips))

# [i] checking 'if x in set' is much faster than 'if x in list' when the collection is large, 
# because sets use hashing internally. For a blacklist of thousands of IPs, a set is the right choice.

# --- find failed login attempts ---
failed = re.findall(r"Failed password for (\w+) from (\S+)", sample_log)
print(f"Failed logins:", failed)

# --- count attempts per IPs (brute force detection) ---
attacker_ips = [ip for _, ip in failed]
counts = Counter(attacker_ips)
print("Atempts counts:", counts)

# [i] '_' is a valid Python variable name, but by convention it means "I don't care about this value". 
# It's a signal to anyone reading the code that the first element is intentionally being thrown away.

# flag IPs with more than 2 attempts
for ip, count in counts.items():
    if count > 2:
        print(f"[!] Possible brute force: {ip} ({count} attempts)")

# --- parse a real log file ---
def parse_ssh_log(filepath):
    failed = []
    with open(filepath, "r", errors="ignore") as f:
        for line in f:
            match = re.search(r"Failed password for (\w+) from (\S+)", line)
            if match:
                failed.append({
                    "user": match.group(1),
                    "ip":   match.group(2)
                })
    return failed

# [i] On Linux, SSH logs live at /var/log/auth.log (Debian/Ubuntu) or /var/log/secure (CentOS/RHEL). 
# A real engagement often starts with reading these to understand who's been accessing the system.

# ------------
# Exercise: Using the sample_log string from the lesson, 
# write a function `find_brute_force(log, threshold)` 
# that returns a list of IPs that have more failed login attempts than the threshold. 
# Test with threshold=2 — it should flag 10.0.0.5.
def find_brute_force(log, threshold):
    failed = re.findall(r"Failed password for (\w+) from (\S+)", log)
    counts = Counter(failed)
    return [ip for ip, count in counts.items() if count > threshold]

print(find_brute_force(sample_log, 2))