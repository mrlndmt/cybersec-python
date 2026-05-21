from scapy.all import IP, TCP, sr1, sniff

# --------------
# scapy - packet crafting and sniffing (advanced but powerful)
# --------------

# scapy lets you build and send raw network packets
# Install: pip install scapy
# Requires admin/root privileges to run

# --- craft a TCP SYN packet manually ---
# This is what a SYN scan looks like under the hood

packet = IP(dst="45.33.32.156") / TCP(dport=80, flags="S")
# IP()  = IP layer - set destination
# TCP() = TCP layer - set port and flags
# "S"   = SYN flag (initiates connection)
# /     = layer stacking operator (not division)

# --- send and receive one response ---
response = sr1(packet, timeout=1, verbose=0)

if response is None:
    print("No response - filtered")
elif response[TCP].flag == "SA":        # SYN-ACK
    print("Port open")
elif response[TCP].flag == "RA":        # RST-ACK
    print("Port closed")

# --- why SYN scan is stealthier than connect scan ---
# connect_ex()      = completes the full TCP handshake (SYN > SYN-ACK > ACK)
# sr1() with S      = only sends SYN, reads SYN-ACK, never send ACK
# Half-open         = less likely to appear in application logs

# --- packet sniffing ---
def handle_packet(pkt):
    if pkt.haslayer(TCP):
        print(f"{pkt[IP].src}:{pkt[TCP].sport} -> "
              f"{pkt[IP].dst}:{pkt[TCP].dport}")

# --- capture 10 TCP packets on the network ---
sniff(filter="tcp", prn=handle_packet, count=10)

# --- scapy layer cheat sheet ---
# IP(dst="x.x.x.x")         = IP layer
# TCP(dport=80, flags="S")  = TCP layer
# UDP(dport=53)             = UDP layer
# ICMP()                    = pint packet
# /                         = stack layer together

# [i] Scapy is a rabbit hole — you can rebuild nmap, write custom exploits, 
# forge packets, sniff traffic. For now just understand the concept. 
# Come back to it once threading and requests feel comfortable.

# /!\ Scapy requires root/admin privileges. 
# On Windows you also need Npcap installed. 
# Use it only in lab environments — sending raw packets on a network you don't own is illegal.

# ------------
# Exercise: This one is conceptual — no running required. 
# Read the SYN scan code above and answer: 
# (1) what does the / operator do in scapy ?
# it permits to stack layers together in a single packet. /!\ order matters: IP() / TCP()

# (2) what is the difference between a SYN scan and a connect scan ?
# a SYN scan is stealthier than the connect scan because it only sends SYN, reads SYN-ACK and never sends ACK
# plus, a half-open connection is less likely to appear in app logs.

# (3) why would a SYN-ACK response mean the port is open ?
# SYN-ACK is the response sent by the server's service port. If it sends it, it means the connection was successful.
