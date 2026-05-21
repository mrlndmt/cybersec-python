# Error handling
# -------------
import socket

# Without error handling - crashes on failure
# sock.connect(("bad_host", 80))            # 'ConnectionRefusedError' !

# With try/except - handle failure gracefully
def check_port(ip, port, timeout=1):
    try:
        sock = socket.socket()
        sock.settimeout(timeout)
        sock.connect((ip, port))            
        sock.close()
        return "OPEN"
    except socket.timeout:
        return "TIMEOUT"
    except ConnectionRefusedError:
        return "CLOSED"
    except OSError as e:
        return f"error: {e}"

result = check_port("192.168.1.1", 80)
print(result)

# Multiple execpt blocks - handle different errors differently
def read_target_file(path):
    try:
        with open(path, "r") as f:
            return f.readlines()                        # 'readlines()' reads the entire file and returns it as a list one item per line
    except FileNotFoundError:
        print(f"[-] File not found: {path}")
        return []                                       # returns an empty list instead of crashing. 'return None' would crash the 'for' loop
    except PermissionError:                             # with: "TypeError: 'NoneType' is not iterable".
        print(f"[-] No permission to read: {path}")
        return []

# 'finally' - always runs, even if there's an exception
def connect_with_cleanup(ip, port):
    sock = socket.socket()
    try:
        sock.connect((ip, port))
        return sock.recv(1024)                          # If connection succeeds, it listens for data coming back from server
    except Exception as e:                              # receiving 1024 bytes max at once. In hacking it's called "banner grabbing"
        print(f"[-] Failed: {e}")                       # because many services (ssh, ftp) send greeting msg when you connect.
        return None
    finally:
        sock.close()                                    # always close the socket

# -------------------
# Exercise: Write a function `safe_int(s)` that tries to convert a string to an integer using `int(s)`, 
# and if it fails (ValueError), prints a warning and returns `None`. Test it with `'443'`, `'abc'`, and `''`.
def safe_int(s):
    try:
        return int(s)
    except ValueError:
        print(f"Error: Cannot convert '{s}' to int")
        return None

s = input("Enter a string: ")
safe_int(s)
