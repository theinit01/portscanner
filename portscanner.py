#!/usr/bin/env python3
import socket
import argparse
import sys
import time
from datetime import datetime
import threading

# ANSI escape codes for colors
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

usage = """

Usage: python3 portscanner.py <Target> <Start_Port> <End_Port>


Description:
  This script is a simple port scanner that checks the status of ports within a specified range on a target host.

Arguments:
  - Target: The target host or IP address you want to scan. This should be a valid hostname or IPv4 address.

  - Start_Port: The starting port of the scan range. Provide a port number between 1 and 65535.

  - End_Port: The ending port of the scan range. Specify a port number between 1 and 65535. It should be greater than or equal to the Start_Port.

Optional Arguments:
  --timeout <Timeout>: Specify a custom timeout value in seconds for port connections. Default is 0.5 seconds.

Example:
  python portscanner.py example.com 80 100 --timeout 1.0 --output report.xml 
  This will scan ports 80 to 100 on the host 'example.com' with a custom timeout of 1.0 seconds.
"""


if (len(sys.argv) != 8 and len(sys.argv) != 6 and len(sys.argv) != 4   ):
    print(usage)
    sys.exit()

def parse_arguments():
    parser = argparse.ArgumentParser(description="A simple port scanner.")
    parser.add_argument("Target", help="The target host or IP address to scan.")
    parser.add_argument("Start_Port", type=int, help="The starting port for the scan range.")
    parser.add_argument("End_Port", type=int, help="The ending port for the scan range.")
    parser.add_argument("--timeout", type=float, default=0.5, help="Custom timeout for port connections (default: 0.5 seconds)")
    parser.add_argument("--output", help="File path to save the scan report.")
    return parser.parse_args()

def resolve_target(target):
    try:
        ip = socket.gethostbyname(target)
        return ip
    except socket.gaierror:
        print("[!!] Couldn't resolve the name")
        sys.exit()

def identify_service(port, protocol):
    try:
        service_name = socket.getservbyport(port, protocol)
        return service_name
    except (OSError, socket.error):
        return "Unknown"

def scan_ports_multithread(target, start_port, end_port, timeout):
    open_ports = []
    closed_ports = []
    threads = []

    def scan_port(port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                s.connect((target, port))
                open_ports.append(port)
        except:
            closed_ports.append(port)

    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port, args=(port,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return open_ports, closed_ports

def print_results(target, open_ports, closed_ports, start_port, end_port):
    print(f"Scan report for {target}")
    print("Scanned", end_port - start_port, "ports")
    print("PORT \t STATE \t SERVICE")
    for port in open_ports:
        service=identify_service(port, "tcp")
        print(f"{GREEN} {port} {RESET} \t {GREEN}open{RESET} \t {service}")
    if len(open_ports) == 0:
        for port in closed_ports:
            service=identify_service(port, "tcp")
            print(f"{RED} {port} {RESET} \t {RED}closed{RESET}\t {service}")



def save_report(output_file, target, open_ports, closed_ports, start_port, end_port):
    with open(output_file, 'w') as file:
        file.write(f"Scan report for {target}\n")
        file.write(f"Scanned {end_port - start_port} ports\n")
        file.write("PORT \t STATE \t SERVICE\n")
        for port in open_ports:
            service = identify_service(port, "tcp")
            file.write(f"{port} \t open \t {service}\n")
        if len(open_ports) == 0:
            for port in closed_ports:
                service = identify_service(port, "tcp")
                file.write(f"{port} \t closed \t {service}\n")

if __name__ == "__main__":
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    start_time = time.time()
    print("Started scan at", dt_string)

    args = parse_arguments()
    target = resolve_target(args.Target)
    open_ports, closed_ports = scan_ports_multithread(target, args.Start_Port, args.End_Port, args.timeout)

    if args.output:
        save_report(args.output, target, open_ports, closed_ports, args.Start_Port, args.End_Port)
        print_results(target, open_ports, closed_ports, args.Start_Port, args.End_Port)
    else:
        print_results(target, open_ports, closed_ports, args.Start_Port, args.End_Port)

    end_time = time.time()
    print()
    print("Scan completed in %.2f seconds" % (end_time - start_time))


# if __name__ == "__main__":
#     now = datetime.now()
#     dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
#     start_time = time.time()
#     print("Started scan at", dt_string)

#     args = parse_arguments()
#     target = resolve_target(args.Target)
#     open_ports, closed_ports = scan_ports_multithread(target, args.Start_Port, args.End_Port, args.timeout)
#     print_results(target, open_ports, closed_ports, args.Start_Port, args.End_Port)  
      
#     end_time = time.time()
#     print()
#     print("Scan completed in %.2f seconds" % (end_time-start_time))