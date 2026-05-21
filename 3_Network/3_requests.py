# requests - HTTP calls, web scraping, REST APIs
# ---------------
import requests

# [i] HTTP RESPONSE STATUS CODES
# Informational responses (100 – 199)
# Successful responses (200 – 299)
# Redirection messages (300 – 399)
# Client error responses (400 – 499)
# Server error responses (500 – 599)

# --- basic GET request ---
response = requests.get("http://scanme.nmap.org")
print(response.status_code)
print(response.headers)
print(response.text[:500])

# --- useful response attributes ---
r = requests.get("https://httpbin.org/get")
print(r.status_code)
print(r.headers["Content-Type"])
print(r.url)
print(r.elapsed)

# --- grabbing HTTP headers (fingerprinting) ---
def get_headers(url):
    try:
        r = requests.get(url, timeout=3)
        return dict(r.headers)
    except requests.exceptions.RequestException as e:
        print(f"[-] Failed: {e}")
        return {}

headers = get_headers("http://scanme.nmap.org")
for key, val in headers.items():
    print(f" {key}: {val}")

# [i] interesting headers to look for:
# Server        → Apache/2.4.41, nginx/1.18 (version info)
# X-Powered-By  → PHP/7.4.3 (tech stack)
# Set-Cookie    → session tokens, flags
# 
# The Server and X-Powered-By headers often reveal exact software versions — useful for finding known CVEs. 
# Always check headers before anything else when assessing a web target.

# --- custom headers (bypass basic filters) ---
headers = {"User-Agent": "Mozilla/5.0"}
r = requests.get("https://httpbin.org/get", headers=headers)

# --- disable SSL verification (for lab targets) ---
r = requests.get("https://target.local", verify=False)

# --- POST request (login, forms, API calls) ---
payload = {"username": "admin", "password": "test"}
r = requests.post("https://httpbin.org/post", data=payload)
print("\n", r.status_code, "\n")

# /!\ Never use requests.get() with verify=False 
# against real targets without understanding the risk
# it disables certificate validation entirely.

# -------------------
# Exercise: Write a function called `fingerprint(url)` that makes a GET request and prints: 
# the status code, the Server header (if present), the X-Powered-By header (if present), 
# and whether the response contains a login form (check if 'password' appears in r.text). 
# Test it on http://scanme.nmap.org
def fingerprint(url):
    try:
        r = requests.get(url, timeout=3)
        result = {
            "status":     r.status_code,
            "server":     r.headers.get("Server", "not found"),
            "powered_by": r.headers.get("X-Powered-By", "not found"),
            "login_form": "password" in r.text.lower()
        }
        print(f"[+] Fingerprint results: {url}")
        print(f"- status code:  {result['status']}")
        print(f"- server:       {result['server']}")
        print(f"- framework:    {result['powered_by']}")

        if result["login_form"]:
            print("\n[+] Login form detected")
        else:
            print("\n[-] No login form found")
        
        return result
    
    except requests.exceptions.RequestException as e:
        print(f"[-] Failed: {e}")
        return {}

data = fingerprint("http://scanme.nmap.org")
if data.get("login_form"):
    print("worth investigating further")
