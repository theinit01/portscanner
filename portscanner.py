#!/usr/bin/env python3
import socket
import argparse
import sys
import time
from datetime import datetime

# ANSI escape codes for colors
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

usage = """
Usage: python3 portscanner.py [options] Target

Description:
  This script is a simple port scanner that checks the status of ports within a specified range on a target host.

Arguments:
  - Target: The target host or IP address you want to scan. This should be a valid hostname or IPv4 address.

Options:
  -h, --help              Show this help message and exit.
  -s, --start-port        The starting port of the scan range. Provide a port number between 1 and 65535. (default: 1)
  -e, --end-port          The ending port of the scan range. Specify a port number between 1 and 65535. It should be greater than or equal to the start port. (default: 65535)
  -r, --range             Specify a specific range of ports to scan (e.g., 80-100). If provided, this option takes precedence over start and end ports.
  -x, --exclude           Specify ports to skip during the scan (e.g., 22,80,443). Ports should be comma-separated.
"""

def parse_arguments():
    parser = argparse.ArgumentParser(description="A simple port scanner.", usage=usage)
    parser.add_argument("Target", help="The target host or IP address to scan.")
    parser.add_argument("-s", "--start-port", type=int, default=1, help="The starting port for the scan range.")
    parser.add_argument("-e", "--end-port", type=int, default=65535, help="The ending port for the scan range.")
    parser.add_argument("-r", "--range", help="Specify a specific range of ports to scan (e.g., 80-100).")
    parser.add_argument("-x", "--exclude", help="Specify ports to skip during the scan (e.g., 22,80,443).")
    return parser.parse_args()

def parse_port_range(port_range):
    try:
        start, end = map(int, port_range.split("-"))
        return start, end
    except ValueError:
        print("Invalid port range format. Use 'start-end' format (e.g., 80-100).")
        sys.exit()

def resolve_target(target):
    try:
        ip = sock   et.gethostbyname(target)
        return ip
    except socket.gaierror:
        print("[!!] Couldn't resolve the name")
        sys.exit()

def scan_ports(target, start_port, end_port, excluded_ports):
    open_ports = []
    closed_ports = []
    for port in range(start_port, end_port + 1):
        if port not in excluded_ports:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(0.5)
                    s.connect((target, port))
                    open_ports.append(port)
            except:
                closed_ports.append(port)
    return open_ports, closed_ports

def print_results(target, open_ports, closed_ports, start_port, end_port):
    print(f"Scan report for {target}")
    print("Scanned", end_port - start_port, "ports")
    print("PORT \t STATE")
    for port in open_ports:
        print(f"{GREEN} {port} {RESET} \t {GREEN}open{RESET}")
    if len(open_ports) == 0:
        for port in closed_ports:
            print(f"{RED} {port} {RESET} \t {RED}closed{RESET}")

if __name__ == "__main":
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    start_time = time.time()
    print("Started scan at", dt_string)

    args = parse_arguments()
    target = resolve_target(args.Target)

    # Handle the port range and excluded ports
    if args.range:
        start_port, end_port = parse_port_range(args.range)
    excluded_ports = set(map(int, args.exclude.split(",")) if args.exclude else [])

    open_ports, closed_ports = scan_ports(target, start_port, end_port, excluded_ports)
    print_results(target, open_ports, closed_ports, start_port, end_port)

    end_time = time.time()
    print()
    print("Scan completed in %.2f seconds" % (end_time - start_time))
