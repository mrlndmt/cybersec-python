import requests

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
