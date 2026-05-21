from urllib.parse import urlparse, urlencode, quote, urljoin

# -----------------
# urllib - URL parsing and encoding: understanding web requests
# -----------------

# urllib.parse breaks URLs apart and builds them back up
# Useful for understanding and manipulating web requests

# --- urlparse: dissect a URL into its components ---
url = "https://target.com:8080/login?user=admin&redirect=/dashboard"
parsed = urlparse(url)

print(parsed.scheme)            # https
print(parsed.netloc)            # target.com:8080
print(parsed.hostname)          # target.com
print(parsed.port)              # 8080
print(parsed.path)              # /login
print(parsed.query)             # user=admin&redirect=/dashboard

# --- extract query parameters ---
from urllib.parse import parse_qs
params = parse_qs(parsed.query)
print("\n", params, "\n")

# --- spot injection points ---
# Any parmeter in the URL is a potential injection target
for param, value in params.items():
    print(f"[*] Parameter found: {param} = {value[0]}")

# --- urlencode: build query strings ---
payload = {"user": "admin' OR '1'='1", "pass": "anything"}
encoded = urlencode(payload)
print("\n", encoded)

# --- quote: encode a simple value ---
path = quote("/etc/passwd")
print("\n", path, "\n")

# --- urljoin: safely combine base URL with a path ---
base = "https://target.com/app/"
print(urljoin(base, "admin"))
print(urljoin(base, "/admin"))
print(urljoin(base, "../secret\n"))

# [i] urlparse is how you find injection points automatically — 
# parse the URL, loop through the parameters, and you have a list of everything worth testing. 
# This is the foundation of automated web scanners.

# ---------------
# Exercise: Write a function called `find_params(url)` that parses a URL 
# and returns a list of parameter names found in the query string. 
# Test it on: 'https://example.com/search?q=test&page=1&sort=asc' — it should return ['q', 'page', 'sort'].
def find_params(url):
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    for param in params.items():
        print(f"[*] Parameter found: {param}")

url = "https://example.com/search?q=test&page=1&sort=asc"
find_params(url)

# OR to be more accurate with output as the exercise asks
def find_params2(url):
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    return list(params.keys())

url = "https://example.com/search?q=test&page=1&sort=asc"
print(find_params2(url))