# web directory fuzzer - find hidden paths on a web server
# ---------------------
import requests
import threading

# A directory fuzzer sends requests to common paths 
# and records which ones exist (200) vs don't (404)

found = []
fuzz_lock = threading.Lock()
fuzz_sem = threading.Semaphore(20)      # fewer threads for HTTP

def check_path(base_url, path):
    with fuzz_sem:
        url = f"{base_url}/{path}"
        try:
            r = requests.get(url, timeout=3, allow_redirects=False)
            if r.status_code not in [404, 400]:
                with fuzz_lock:
                    found.append((path, r.status_code))
                    print(f"[+] {r.status_code} - {url}")
        except requests.exceptions.RequestException:
            pass                        # ignore connection errors

def fuzz(base_url, wordlist_path):
    with open(wordlist_path, "r", errors="ignore") as f:
        paths = [line.strip() for line in f if line.strip()]
        # same as:
        paths = []
        for line in f:
            line = line.strip()
            if line:
                paths.append(line)    
    
    print(f"[*] Fuzzing {base_url} with {len(paths)} paths")
    threads = []
    for path in paths:
        t = threading.Thread(target=check_path, args=(base_url, path))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    return found

# Common paths worth checking even without a wordlist:
common = ["admin", "login", "dashboard", "config", "backup",
          "robots.txt", ".git", "api", "uploads", "phpmyadmin"]

for path in common:
    check_path("scanme.nmap.org", path)

# [i] 'robots.txt' tells search engines what not to index — 
# which means it often lists the exact paths an admin wants to hide. 
# Always check it first before fuzzing.

# /!\ Directory fuzzing generates lots of HTTP requests quickly. 
# Never fuzz a target without permission; it's easy to detect and constitutes unauthorized access.

# -----------
# Exercise: Write a `check_path()` function that takes a base URL and a path, 
# makes a GET request, and prints the status code and URL if the response is not 404. 
# Test it against http://scanme.nmap.org 
# with this list: ['index.html', 'admin', 'robots.txt', 'login', '.git', 'backup']
def check_path(base_url, path):
    url = f"{base_url}/{path}"
    try:
        r = requests.get(url, timeout=3, allow_redirects=False)
        if r.status_code != 404:
            print(f"[+] {r.status_code} - {url}")
        else:
            print(f"[-] 404 - {url}")
    except requests.exceptions.RequestException as e:
        print(f"[-] Error: {e}")

paths = ["index.html", "admin", "robots.txt", "login", ".git", "backup"]
for path in paths:
    check_path("http://scanme.nmap.org", path)
