# json & csv - save structured results, parse API responses
# ------------
import json
import csv
import os

# --- JSON - perfect for saving scan results ---

# Python dict -> JSON file
scan_result = {
    "target": "192.168.1.1",
    "open_ports": [22, 80, 443],
    "os": "Linux",
    "timestamp": "2024-01-15"
}

print(f"Saving to: {os.getcwd()}")              # tells where the file was saved (where the python code is executed from)

with open("result.json", "w") as f:
    json.dump(scan_result, f, indent=4)         # indent=4 makes it more readable

# JSON file -> Python dict
with open("result.json", "r") as f:
    loaded = json.load(f)

print(loaded["target"])
print(loaded["open_ports"])

# JSON string <-> dict (useful for API responses)
raw = '{"status": "open", "port": 80}'
data = json.loads(raw)                       # string -> dict
back = json.dumps(data)                      # dict -> string

# --- CSV - great for spreadsheet-friendly reports ---

# Write a CSV report
hosts = [
    {"ip": "192.168.1.1",  "port": 80,  "status": "open"},
    {"ip": "192.168.1.1",  "port": 443, "status": "open"},
    {"ip": "192.168.1.10", "port": 22,  "status": "open"},
]

print(f"Saving to: {os.getcwd()}")

with open("report.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["ip","port","status"])
    writer.writeheader()
    writer.writerows(hosts)

# Read a CSV back
with open("report.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"{row['ip']}:{row['port']} - {row['status']}")

# --- Use an absolute path based on where the script lives to save the file ---
import os
import json

# __file__ is a built-in variable that holds the path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(script_dir, "result.json")

scan_result = {
    "target": "192.168.1.1",
    "open_ports": [22, 80, 443],
    "os": "Linux",
    "timestamp": "2024-01-15"
}

with open(output_path, "w") as f:
    json.dump(scan_result, f, indent=4)

print(f"Saved to: {output_path}")

# Note: Save scan results as JSON during a pentest — it keeps the full structure and you can reload it later. 
# Use CSV when you need to share results with a client or open them in Excel.

# -----------
# Exercise: Create a list of 3 dicts, each with keys 'ip', 'open_ports' (a list), and 'hostname'. 
# Save it to a JSON file with indent=4. 
# Then reload it and loop through printing each host's IP and how many open ports it has.
hosts = [
    {"ip": "192.168.1.1",  "open_port": [22, 80],  "hostname": "target1"},
    {"ip": "192.168.1.1",  "open_port": [21, 443],  "hostname": "target2"},
    {"ip": "192.168.1.10", "open_port": [],  "hostname": "target3"}
]

with open("results.json", "w") as f:
    json.dump(hosts, f, indent=4)

with open("results.json", "r") as f:
    reader = json.load(f)
    for row in reader:
        print(f"{row['ip']} - open ports: {len(row['open_port'])}")
