# Functions
# ----------
# Define a function with 'def'
def scan_port(ip, port):
    """Check if a port is open (mock version)."""
    print(f"Scanning {ip}:{port}")
    return True                     # 'return' sends a value back

# Call the function
result = scan_port("10.0.0.1", 80)
print(result)

# Default arguments - port defaults to 80 if not given
def connect(ip, port=80, timeout=2):
    print(f"Connecting to {ip}:{port} (timout={timeout}s)")

connect("10.0.0.1")                 # default port, default timeout
connect("10.0.0.1", 443)            # port=443, default timeout
connect("10.0.0.1", timeout=5)      # default port, timeout=5

# Return multiple values (as a tuple)
def get_target_info(raw_input):
    try:
        parts   = raw_input.split(":")  # 'parts' cuts the string at every colon and returns a list of the pieces
        ip      = parts[0]              # grabs the first element of the list, stays a string
        port    = int(parts[1])         # grabs the second element of the list, converts it to 'int'
        return ip, port                 # returns 2 values at once, Python packs them into a tuple automatically
    except (IndexError, ValueError):
        print(f"[-] Invalid target format: '{raw_input}' — expected IP:PORT")
        return None, None

host, port = get_target_info("192.168.1.1:8000")
print(host, port)

# Functions can call other functions
def run_scan(target_str):
    ip, port = get_target_info(target_str)
    scan_port(ip, port)

run_scan("10.0.0.5:22")

# -------------
# Exercise: Write two functions: 
# 1: `parse_target(s)` that takes a string like `'192.168.1.1:443'` and returns the IP and port separately, 
# 2: `report(ip, port, status)` that prints a formatted line like `[OPEN] 192.168.1.1:443`. Call them together.

def parse_target(s):
    ip, port = s.split(":")
    return ip, int(port)

def report(ip, port, status):
    print(f"\n[{status.upper()}] {ip}:{port}")      # 'status.upper()' puts 'status' value in CAPITALS

ip, port = parse_target("10.2.2.11:443")
report(ip, port, "open")
