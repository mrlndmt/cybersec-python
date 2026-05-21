# threading - parallel port scan makes scanner faster
# ------------------
import threading
import socket
 
 # Without threading, scanning 1024 ports at 1s timeout = 17min
 # With threading, scanning 1024 ports with 100 threads = 10sec

 # --- basic thread example ---
def worker(name):
    print(f"Thread {name} running")

threads = []                                            # empty list to keep track of thread created before .join()
for i in range(5):
    t = threading.Thread(target=worker, args=(i,))      # create thread object for function scan_port
    threads.append(t)
    t.start()

for i in threads:
    t.join()                                            # wait for all threads to finish
print("All done")

# --- threaded port scanner ---
open_ports = []
lock = threading.Lock()                                 # prevent threads writing at the same time

# /!\ The lock is critical — without it two threads might try 
# to append to open_ports at the same time and corrupt the list. 
# Always use a lock when multiple threads write to the same variable.

def scan_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    if sock.connect_ex((ip, port)) == 0:
        with lock:                                      # only one thread writes at a time
            open_ports.append(port)
            print(f"[+] Port {port} open")
    sock.close()

# launch one thread per port
target = "45.33.32.156"
threads = []
for port in range(1, 9999):
    t = threading.Thread(target=scan_port, args=(target, port))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"\nOpen ports: {sorted(open_ports)}")

# --- thread limiting with Semaphore ---
# 1024 threads at once can overwhelm the system
# Semaphore limits how many run simultaneously
sem = threading.Semaphore(100)                          # max 100 threads at once

def scan_limited(ip, port):
    with sem:
        scan_port(ip, port)

# ---------------
# Exercise: Upgrade your scan_range() function from the socket lesson to use threading. 
# Each port gets its own thread, use a lock to protect the results list, 
# and use a Semaphore to limit to 100 concurrent threads. 
# Compare the speed difference against your original version.
#
# see 2_threadingExercise
