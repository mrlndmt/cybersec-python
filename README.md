# Python for Ethical Hacking — Learning Project

A progressive Python learning project focused on building practical security tools from scratch. Each phase builds on the previous, culminating in real recon and enumeration tools.

---

## Structure

```
├── 1_Foundation/        # Core Python syntax
├── 2_Toolbox/           # Standard library modules
│   └── Project_CLI_Tool/    # Phase 2 mini-project: CLI recon tool
├── 3_Network/           # Networking and socket programming
│   └── Project_Scanner/     # Phase 3 mini-project: multithreaded port scanner
└── 4_Hacking_Scripts/   # Offensive tooling
    └── Project_Toolkit/     # Phase 4 mini-project: recon & enumeration toolkit
```

---

## Phases

### Phase 1 — Foundation
Core Python refresher with security-oriented examples: variables, control flow, functions, lists and dicts, file I/O, and error handling.

### Phase 2 — Toolbox
Standard library modules used in real scripts: `os`, `sys`, `argparse`, `re`, `subprocess`, `json`, `csv`, `datetime`.

**Mini-project:** A CLI recon tool that validates a target, pings the host, grabs the SSH banner, and saves a timestamped JSON report.

```bash
py CLIReconTool.py -t 192.168.1.1 -p 22 -v -o
```

### Phase 3 — Networking
Network programming with `socket`, `requests`, `urllib`, and `threading`. Covers TCP connect scanning, HTTP fingerprinting, URL parsing, and multithreaded scanning.

**Mini-project:** A multithreaded port scanner with web fingerprinting and structured JSON output.

```bash
py ProjectPhase3.py -t scanme.nmap.org -s 1 -e 1024 -v -o
```

Sample output:
```json
{
    "target": "scanme.nmap.org",
    "ip": "45.33.32.156",
    "open_ports": [22, 80],
    "banners": {
        "22": "SSH-2.0-OpenSSH_6.6.1p1 Ubuntu-2ubuntu2.13"
    },
    "http": {
        "status": 200,
        "server": "Apache/2.4.7 (Ubuntu)",
        "login_form": true
    }
}
```

### Phase 4 — Hacking Scripts
Practical offensive tools: port scanner with progress counter, wordlist password attack, web directory fuzzer, SSH log parser, and subdomain enumerator.

---

## Tools Built

| Tool | Description | Key modules |
|------|-------------|-------------|
| CLI recon tool | Ping, banner grab, JSON report | `socket`, `subprocess`, `argparse`, `json` |
| Port scanner | Multithreaded, 1-65535 range | `socket`, `threading` |
| Web fingerprinter | Headers, server version, login form detection | `requests` |
| Directory fuzzer | Threaded HTTP path enumeration | `requests`, `threading` |
| Password attack | Wordlist and brute force | `itertools` |
| Log parser | Brute force detection from SSH logs | `re`, `collections` |
| Subdomain enumerator | DNS resolution over wordlist | `socket`, `threading` |

---

## Usage

All tools use a consistent CLI interface:

```bash
py tool.py -t <target> [-p <port>] [-s <start>] [-e <end>] [-v] [-o]

-t   Target IP or hostname
-p   Port (where applicable)
-s   Port range start
-e   Port range end
-v   Verbose output
-o   Save JSON report
```

---

## Legal notice

All tools in this repository are built for educational purposes and for use in authorized lab environments only (local VMs, TryHackMe, HackTheBox, or targets with explicit written permission). Unauthorized scanning or attacking of systems is illegal.

---

## Environment

- Python 3.x
- `pip install requests` for web modules
- Tested on Windows 10/11 with `py` launcher
- Compatible with Kali Linux (`python3`)
