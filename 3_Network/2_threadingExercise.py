# Threading - Exercise
# --------------------
# --------------------
# Exercise: Upgrade your scan_range() function from the socket lesson to use threading. 
# Each port gets its own thread, use a lock to protect the results list, 
# and use a Semaphore to limit to 100 concurrent threads. 
# Compare the speed difference against your original version.
# --------------------
import socket
import threading

# shared list where all threads store their results
open_ports = []

# lock prevents two threads writing to open_ports at the same time
lock = threading.Lock()

# semaphore limits how many threads run concurrently
sem = threading.Semaphore(100)

# /!\ both 'lock' and 'sem' must be outside the function in order to work /!\

def scan_port(ip, port):
    # aquire a semaphore slot; waits if 100 slots are already assigned
    with sem:
        # create a fresh TCP socket for this scpecific sport
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # don't wait more that 1sec for a response  
        sock.settimeout(1)
        # connect_ex returns 0 if port is open; non-zero if closed/filtered; no exception on failure
        if sock.connect_ex((ip, port)) == 0:
            # aquire the lock before writing to the shared list; only one thread inside this block at a time
            with lock:
                open_ports.append(port)
                print(f"[+] Port {port} open")
        # always close the socket wheter port was open or not
        sock.close()

def scan_range(ip, start, end):
    # resolves hostname to IP once; if it was in scan_ports() it would resolve everytime, which is useless
    ip = socket.gethostbyname(ip)
    # list to keep track of threads that can be joined later
    threads = []                              
    for port in range(start, end + 1):    
        # create one thread per port; each runs scan_port() independently                              
        t = threading.Thread(target=scan_port, args=(ip, port))
        # store the thread so we can wait for it later
        threads.append(t)
        # launch the thread; start the scan_port() function
        t.start()
    # wait for every thread to finish before returning; without it, function would return before scans complete
    for t in threads:
        t.join()
    # returns ports in numerical order
    return sorted(open_ports)
        
results = scan_range("scanme.nmap.org", 1, 9999)
print(f"Open ports: {results}")
