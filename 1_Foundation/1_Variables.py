# Data Types
# ------------
target_ip = "192.168.1.1"
target_port = 80
timeout = 2.5
is_open = False
response = None

print("IP is", type(target_ip), "\nPort is", type(target_port), 
      "\nTimeout is", type(timeout), "\nis_open is", type(is_open), 
      "\nresponse is", type(response))

# Converting to types (casting)
port_as_str = str(target_port)
port_back = int(port_as_str)

print("\nPort is now", type(port_as_str), "and gets back to", type(port_back))

# f-string: embed variables inside text
print(f"\nScanning {target_ip}:{target_port}")

# ---------------
# Exercise: Create variables for: a target hostname (str), 
# a list of ports to scan (just store the number 3 times as 3 int variables: 22, 80, 443), 
# and a boolean called `verbose`. 
# Then print them all in one f-string like: `Scanning example.com — ports 22 80 443 — verbose: True`
hostname = "example.com"
p1, p2, p3 = 22, 80, 443
verbose = True
print(f"Scanning {hostname} - ports {p1} {p2} {p3} - verbose: {verbose}")