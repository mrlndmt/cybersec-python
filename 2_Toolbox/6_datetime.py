# datetime - timestamp for logs and reports
# ----------
from datetime import datetime

# Get the current date and time
now = datetime.now()
print(now)

# Format it as a readable string
print(now.strftime("%d-%m-%Y %H:%M:%S"))
print(now.strftime("%d/%m/%Y"))

# Practical: timestamped output filename
timestamp = now.strftime("%Y%m%d_%H%M%S")
filename = f"scan_{timestamp}.json"
print(filename)

# Practical: log with timestamp
def log(msg, level="INFO"):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] [{level}] {msg}")

log("Starting scan")
log("Port 80 open", "FOUND")
log("Scan complete")

# --- Measure how long something took ---
start = datetime.now()

# ... your scan runs here ...
import time
time.sleep(1)           # simulate work

end = datetime.now()
elapsed = (end - start).total_seconds()
print(f"\nScan completed in {elapsed:.2f} seconds")       # .2f = two decimals

# Note: Always timestamp your output files — scan_20240115_143207.json instead of scan.json. 
# That way multiple runs never overwrite each other and you have a full audit trail of what you ran and when.

# ----------------
# Exercise: Write a log() function that accepts a message and an optional level (default 'INFO'), 
# and prints: [HH:MM:SS] [LEVEL] message. 
# Then write a function run_task(name) that logs 'Starting ', sleeps 1 second using time.sleep(1), then logs 'Finished ' 
# and prints how many seconds it took.
from datetime import datetime
import time

def log(msg, level="INFO"):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] [{level}] {msg}")

def run_task(name):
    log(f"Starting {name}")
    start = datetime.now()
    time.sleep(1)
    elapsed = (datetime.now() - start).total_seconds()
    log(f"Finished {name} in {elapsed:.2f}s", "DONE")

run_task("port scan")
run_task("banner grab")
