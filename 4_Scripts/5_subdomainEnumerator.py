# subdomain enumerator - DNS lookup to find subdomains
# ----------------------
import socket
import threading

# Subdomain enumeration finds hidden services on a domain
# like: mail.target.com, dev.target.com, admin.target.com, etc

found_subs = []
sub_lock = threading.Lock()
sub_sem = threading.Semaphore(50)

def check_subdomain(domain, sub):
    with sub_sem:
        hostname = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(hostname)
            with sub_lock:
                found_subs.append((hostname, ip))
                print(f"[+] {hostname} -> {ip}")
        except socket.gaierror:
            pass                    # NXDOMAIN - subdomain doesn't exist

def enumerate_subdomain(domain, wordlist):
    print(f"[*] Enumerating subdomains for {domain}")
    threads = []
    for sub in wordlist:
        t = threading.Thread(target=check_subdomain, args=(domain, sub))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    return found_subs

# common subdomains wordlist
common_subs = [
    "www", "mail", "ftp", "dev", "staging", "admin",
    "api", "vpn", "remote", "portal", "blog", "shop",
    "test", "beta", "cdn", "static", "assets", "ns1", "ns2"
]

# [i] Real subdomain wordlists have tens of thousands of entries. 
# SecLists on GitHub has the best collection - 
# subdomains-top1million-5000.txt is a good starting point for most engagements.

results = enumerate_subdomain("nmap.org", common_subs)
print(f"\nFound {len(results)} subdomains")