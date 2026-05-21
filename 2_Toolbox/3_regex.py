# re (regex) - find patterns in text - IP, email, tokens
# --------------
# regex is constantly used for log parsing — pulling IPs, emails, usernames, tokens out of messy text
import re

# Regex lets you search for patterns instead of exact things
text = "Server at 192.168.1.10 responded. Admin: admin@corp.com"

# re.findall() - return ALL matches as a list
ip_pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"      # \d = any digit; '{1,3}' = repeat the previous thing between 1 and 3 times; \. = literal dot '.'
ips = re.findall(ip_pattern, text)
print(ips)

email_pattern = r"[\w.+-]+@[\w-]+\.[a-z]{2,}"           # [...] = match any one character from this set; \w = any letter, digit, underscore;
emails = re.findall(email_pattern, text)
print(emails)

# re.search() - find the FIRST match (or None)
match = re.search(r"Admin: (\S+)", text)                # \S+ = anything that's NOT a space, tab, newline; + = here it means one or more of those
if match:                                               # it takes everything after having found "Admin: "
    print(match.group(1))

# re.sub() - find and replace
clean = re.sub(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", "[REDACTED]", text)   # "[REDACTED]" will replace the IP address in a new string ("clean")
print(clean)                                                                # it doesn't alter the original variable ("text")

# Practical example: extract IPs from a log file
log = """
Failed login from 10.0.0.5
Port scan detected from 10.0.0.99
Normal request from 10.0.0.1
"""
attackers = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", log)
print(set(attackers))

# Common pattern cheat sheet:
# \d       = any digit 0-9
# \d{1,3}  = 1 to 3 digits
# \w       = letter, digit, or underscore
# \S       = any non-whitespace character
# .         = any character
# +         = one or more
# *         = zero or more
# ?         = zero or one (optional)

#------------------
# Exercise: Given the string: 
# 'User john logged in from 172.16.0.5. User alice logged in from 10.10.10.2. Contact: sec@target.com'. 
# Write regex to extract: 
# (1) all IP addresses, 
# (2) all usernames (the word after 'User '), 
# (3) the email address.
log1 = "User john logged in from 172.16.0.5. User alice logged in from 10.10.10.2. Contact: sec@target.com"

ips = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", log1)
usernames = re.findall(r"User (\w+)", log1)
emails = re.findall(r"[\w.+-]+@[\w-]+\.[a-z]{2,}", log1)

print("IPs: ", ips)
print("User: ", usernames)
print("Emails: ", emails)

