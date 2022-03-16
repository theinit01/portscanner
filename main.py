#!/usr/bin/env python3
import socket
import sys
import time
from datetime import datetime

usage = "Usage: python3 scanner.py [Target] [Start_Port] [End_Port]"

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
    print(f"{ports} \t open")

if len(open_ports) == 0:
    for ports in closed_ports:
        print(f"{ports} \t closed")

end_time = time.time()

print()
print("Scan completed in %.2f seconds" % (end_time-start_time))
