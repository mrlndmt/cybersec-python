# argparse - build CLI tools with flags and options
# ------------------------------
import argparse

# argparse turns your script into a proper command-line tool
# Usage: python3 scanner.py -t 192.168.1.1 -p 80 --verbose

parser = argparse.ArgumentParser(
    description="Simple port scanner"
)

# Required argument - must always be provided
parser.add_argument(
    "-t", 
    "--target",
    required=True,
    help="Target IP address"
)

# Optional argument with a default value
parser.add_argument(
    "-p",
    "--port",
    type=int,
    default=80,
    help="Port to scan (default: 80)"
)

# Flag - True if present, False if absent
parser.add_argument(
    "-v",
    "--verbose",
    action="store_true",
    help="Enable verbose output"
)

# Optional output file
parser.add_argument(
    "-o",
    "--output",
    help="Save results to this file"
)

# Parse what the user typed
args = parser.parse_args()

# Access the values
print(f"Target  : {args.target}")
print(f"Port    : {args.port}")
print(f"Verbose : {args.verbose}")

if args.output:
    print(f"Saving to: {args.output}")

# argparse auto-generates --help for free:
# python3 scanner.py --help

# ------------------
# Exercise: Build a CLI tool called 'pinger.py' using argparse with: 
# a required -t/--target flag (string), 
# an optional -c/--count flag (integer, default 4), 
# and a -v/--verbose flag (store_true). 
# Print the parsed values in a neat summary. 
# Test it by running: python3 pinger.py -t 10.0.0.1 -c 10 -v
import argparse

pinger = argparse.ArgumentParser(description="Simple ping tool")

pinger.add_argument("-t", "--target", required=True, help="Target IP")
pinger.add_argument("-c", "--count", type=int, default=4, help="Count - default: 4")
pinger.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

args = pinger.parse_args()

print(f"Target: {args.target}\nCount: {args.count}\nVerbose: {args.verbose}")
