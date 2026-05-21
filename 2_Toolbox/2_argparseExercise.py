# --- argparse - Exercise --- 
# Build a CLI tool called 'pinger.py' using argparse with: 
# a required -t/--target flag (string), 
# an optional -c/--count flag (integer, default 4), 
# and a -v/--verbose flag (store_true). 
# Print the parsed values in a neat summary. 
# Test it by running: python3 pinger.py -t 10.0.0.1 -c 10 -v
import argparse

pinger = argparse.ArgumentParser(description="Simple ping tool")

pinger.add_argument("-t", "--target",   required=True,          help="Target IP")
pinger.add_argument("-c", "--count",    type=int, default=4,    help="Count - default: 4")
pinger.add_argument("-v", "--verbose",  action="store_true",    help="Verbose output")

args = pinger.parse_args()

print(f"Target: {args.target}\nCount: {args.count}\nVerbose: {args.verbose}")
