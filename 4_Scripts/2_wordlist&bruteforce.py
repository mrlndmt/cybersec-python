# password attack - wordlist iteration; foundation of bruteforce
# -----------------
import itertools
import string

# --- wordlist/dictionary attack ---
# reads passwords from a file and tries each one

def load_wordlist(path):
    try:
        with open(path, "r", errors="ignore") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[-] Wordlist not found: {path}")
        return []
    
def try_login(username, password):
    """Mock login - replace with real logic (SSH, HTTP, FTP, ...)"""
    return password == "4398"      # simulate correct password

def wordlist_attack(username, wordlist_path):
    passwords = load_wordlist(wordlist_path)
    print(f"[*] Loaded {len(passwords)} passwords")
    print(f"[*] Attacking user: {username}")
    
    for i, password in enumerate(passwords):
        print(f"\r[*] Trying {i+1}/{len(passwords)}: {password:<20}", end="", flush=True)
        if try_login(username, password):
            print(f"\n[+] Found: {username}:{password}")
            return password
    print("\n[-] Password not found")
    return None

# --- brute force (generate password) ---
# when you don't have a wordlist - try every combination
# /!\ WARNING: extremely slow for long passwords

def brute_force(username, charset, max_length):
    for length in range(1, max_length + 1):
        for combo in itertools.product(charset, repeat=length):
            password = "".join(combo)
            print(f"\r[*] Trying: {password:<15}", end="", flush=True)
            if try_login(username, password):
                print(f"\n[+] Found: {username}:{password}")
                return password
    return None

# digits only, max 4 chars - manageable
brute_force("admin", string.digits, 4)

# all printable chars, max 8 — would take years
#brute_force("admin", string.printable, 8)

# [i] Dictionary attacks are fast because humans reuse common passwords. 
# Always try a wordlist attack before brute force — 
# rockyou.txt has 14 million real passwords leaked from actual breaches.

# --------------
# Exercise: Write a `wordlist_attack()` function that takes a username 
# and a list of passwords (just use a plain Python list, no file needed). 
# Make `try_login()` return True only for the password 'letmein'. 
# Run the attack against ['password', 'admin', '123456', 'letmein', 'qwerty'] and print found credentials.
def try_login(username, password):
    # mock login setup
    return password == "letmein"

def wordlist_attack(username, passwords):
    for i, password in enumerate(passwords):
        print(f"[*] Trying: {password}")
        if try_login(username, password):
            print(f"[+] Found: {username}:{password}")
            return password
    print("[-] Not found")
    return None

wordlist = ["password", "admin", "123456", "letmein", "qwerty"]
wordlist_attack("admin", wordlist)
