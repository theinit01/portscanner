#!/usr/bin/env python3
import socket
import sys
import time
from datetime import datetime

def get_target_ip(target):
    try:
        return socket.gethostbyname(target)
    except socket.gaierror:
        print("[!!] Couldn't resolve the name")
        sys.exit()

def scan_port(target, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            s.connect((target, port))
            return port
    except:
        return None

def perform_scan(target, start_port, end_port):
    open_ports = []
    closed_ports = []

    for port in range(start_port, end_port + 1):
        result = scan_port(target, port)
        if result:
            open_ports.append(result)
        else:
            closed_ports.append(port)

    return open_ports, closed_ports

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 scanner.py [Target] [Start_Port] [End_Port]")
        sys.exit()

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    start_time = time.time()

    print("Started scan at", dt_string)

    target = get_target_ip(sys.argv[1])
    start_port = int(sys.argv[2])
    end_port = int(sys.argv[3])

    open_ports, closed_ports = perform_scan(target, start_port, end_port)

    print(f"Scan report for {target}")
    print(f"Scanned {end_port - start_port} ports")
    print("PORT \t STATE")

    for port in open_ports:
        print(f"{port} \t open")

    if not open_ports:
        for port in closed_ports:
            print(f"{port} \t closed")

    end_time = time.time()

    print()
    print("Scan completed in %.2f seconds" % (end_time - start_time))

if __name__ == "__main__":
    main()
