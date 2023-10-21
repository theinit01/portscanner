#!/usr/bin/env python3
import socket
import sys
import time
from datetime import datetime

# ANSI escape codes for colors
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

usage = """
Usage: python3 scanner.py <Target> <Start_Port> <End_Port>

Description:
  This script is a simple port scanner that checks the status of ports within a specified range on a target host.

Arguments:
  - Target: The target host or IP address you want to scan. This should be a valid hostname or IPv4 address.

  - Start_Port: The starting port of the scan range. Provide a port number between 1 and 65535.

  - End_Port: The ending port of the scan range. Specify a port number between 1 and 65535. It should be greater than or equal to the Start_Port.

Example:
  python3 scanner.py example.com 80 100
  This will scan ports 80 to 100 on the host 'example.com'.
"""

if (len(sys.argv) != 4):
    print(usage)
    sys.exit()

now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
start_time = time.time()

print("Started scan at", dt_string)

try:
    target = socket.gethostbyname(sys.argv[1])
except socket.gaierror:
    print("[!!] Couldn't resolve the name")
    sys.exit()

start_port = int(sys.argv[2])
end_port = int(sys.argv[3])
open_ports = []
closed_ports = []

for port in range(start_port, end_port+1):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            s.connect((target, port))
            open_ports.append(port)
    except:
        closed_ports.append(port)

print(f"Scan report for {target}")
print("Scanned", end_port-start_port, "ports")
print("PORT \t STATE")

for ports in open_ports:
    print(f"{GREEN} {ports} {RESET} \t {GREEN}open{RESET}")

#if len(open_ports) == 0:
for ports in closed_ports:
    print(f"{RED} {ports} {RESET} \t {RED}closed{RESET}")

end_time = time.time()

print()
print("Scan completed in %.2f seconds" % (end_time-start_time))
