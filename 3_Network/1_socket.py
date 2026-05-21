# Socket - TCP/UDP connections, port scanners, banner grabbing
# ---------------
# Socket is the foundation of all network tools
import socket

# ---  hostname resolution ---
ip = socket.gethostbyname("scanme.nmap.org")
print(ip)

# --- TCP connect scan (core of port scanner) ---
def is_port_open(ip, port, timeout=1):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # IPv4 - TCP
    sock.settimeout(timeout)
    result = sock.connect_ex((ip, port))                        # returns 0 if open
    sock.close()
    return result == 0                                          # True = open

print(is_port_open("45.33.32.156", 80))
print(is_port_open("45.33.32.156", 9999))

# --- connect_ex vs connect ---
# connect()     = raise an exception if port is closed
# connect_ex()  = returns an error code instead (0 = success)
# connect_ex is better for scanners - no try/except needed

# --- socket types ---
# AF_INET       = IPv4
# AF_INET6      = IPv6
# SOCK.STREAM   = TCP (reliable, connection-based)
# SOCK.DGRAM    = UDP (fast, connectionless)

# --- scan a range of ports ---
#target = "45.33.32.156"
#for port in range(20, 25):
#    if is_port_open(target, port):
#        print(f"[+] Port {port} open")

# --- UDP example (DNS lookup on port 53) ---
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)         # IPv4 - UDP
sock.settimeout(2)
# UDP doesn't connect — you sendto and recvfrom directly
sock.sendto(b"hello", ("8.8.8.8", 53))

# ---------------
# Exercise: Write a function called `scan_range(ip, start, end)` 
# that scans all ports from start to end and returns a list of open ports. 
# Test it on scanme.nmap.org with ports 1-1024. Print each open port as you find it.
# ---------------
def scan_range(ip, start, end):
    ip = socket.gethostbyname(ip)                                   # resolve the hostname to get ip address
    for port in range(start, end):                                  # socket inside the loop to get -
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # new socket connection for every port
        sock.settimeout(0.5)
        result = sock.connect_ex((ip, port))
        if result == 0:
            print(f"Port {port} open")
    sock.close()

scan_range("scanme.nmap.org", 20, 81)
