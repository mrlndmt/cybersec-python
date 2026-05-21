# Control flow
# -------------
port = 22
status = "open"

# if / elif / else
if status == "open":
    print(f"Port {port} is open - checking service...")
elif status == "filtered":
    print(f"Port {port} is filtered - firewall likely")
else:
    print(f"Port {port} is closed")

# for loop - iterate over a list
ports = [21, 22, 80, 443, 8080]
for p in ports:
    print(f"Checking port {p}...")

# while loop - keep going until a condition is met
attempts = 0
max_attempts = 3
while attempts < max_attempts:
    print(f"Login attempt {attempts + 1}")
    attempts +=1

# break - exit a loop early
for p in ports:
    if p == 80:
        print(f"Found HTTP port: {p}, stopping")
        break

# continue - skip to next iteration
for p in ports:
    if p == 22:
        print(f"Skipping port {p} SSH for now...")
        continue    # skip SSH for now
    print(f"Scanning {p}")

# ------------
# Exercise: Write a loop that goes through ports [21, 22, 23, 25, 80, 443, 3389]. 
# For each port, print whether it's 'well-known dangerous' (21=FTP, 23=Telnet, 3389=RDP) 
# or 'common web/ssh'. Use if/elif/else inside the loop.
target_ports = [21, 22, 23, 25, 80, 443, 3389]
for p in target_ports:
    if p in [21, 23, 3389]:
        print(f"Port {p}: well-known dangerous")
    elif p in [22, 80, 443]:
        print(f"Port {p}: common web/ssh")
    else:
        print(f"Port {p}: other")

