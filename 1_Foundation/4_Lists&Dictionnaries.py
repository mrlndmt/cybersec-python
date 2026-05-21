# Lists & Dictionnaries
# ---------------------

# --- LIST - ordered, access by index, can have duplicates ---
open_ports = [22, 80, 443]
open_ports.append(8080)         # add '8080' to end of the list
open_ports.remove(22)           # remove by value
print(open_ports[0])            # print first item: 80
print(open_ports[-1])           # print last item: 8080
print(len(open_ports))          # print the length of the string (number of values it contains): 3

# Slicing - grab a portion
ports = [21, 22, 80, 443, 8080, 8443]
first_three = ports[:3]
last_two    = ports[-2:]
print(f"\nFirst three values: {first_three}\nLast two values: {last_two}\n")

# List comprehension - build a list in one line
# Get all ports above 1024 (high ports)
high_ports = [p for p in ports if p > 1024]
print(high_ports)

# --- DICT - pairs of 'key:value' like a lookup table ---
host_info = {
    "ip":           "10.3.4.5",
    "hostname":     "webserver01",
    "os":           "Linux",
    "open_ports":   [80, 443, 22]
}

host_info["services"] = ["nginx", "sshd"]                           # add new key

print(host_info["ip"])
print(f'{host_info["hostname"]} - {host_info["services"]}\n')       # notice we used single ' outside because already used double " inside

# Iterate over a dict
for key, value in host_info.items():
    print(f" {key}: {value}")

# Dict of dicts - perfect for scan results
scan_results = {
    "192.1168.1.1": {"open": [80, 443], "os": "unkown"},
    "192.168.1.10": {"open": [22, 80], "os": "Linux"}
}
print(scan_results["192.168.1.10"])

# Dicts are your scan result storage. One dict per host, with keys for open ports, OS, banners, vulnerabilities. 
# Build this habit now — your scripts will be much easier to read and extend.

# ----------------
# Exercise: Create a dict called `hosts` with two IPs as keys. 
# Each value should itself be a dict with `'open_ports'` (a list) and `'status'` ('up' or 'down'). 
# Loop through `hosts.items()` and print a summary line for each host.

hosts = {
    "10.1.1.2":     {"open_ports": [22, 80], "status": "up"},
    "10.1.1.13":    {"open_ports": [], "status": "down"}
}

for ip, info in hosts.items():
    ports = info["open_ports"]
    status = info["status"]
    print(f"\n{ip} [{status.upper()}] - open ports: {ports}")
