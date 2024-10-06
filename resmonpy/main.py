import argparse
import ctypes
import sys
from config import Config
from network import NetworkMonitor
from process import ProcessMonitor
from process import get_pid
from utils import is_admin, parse_arguments, verify_processes


def main():
    if not is_admin():
        print("This script requires administrator privileges. Please run as an administrator.")
        sys.exit(1)

    args = parse_arguments()
    config = Config(directory=args.directory)
    process_names = verify_processes(args.processes)
    process_dict = get_pid(process_names)

    #network_monitor = NetworkMonitor(process_dict=process_dict, interval=args.interval, config=config)
    #network_monitor.start_monitoring()
    process_monitor = ProcessMonitor(process_dict,config=config)
    process_monitor.start_monitoring()


if __name__ == "__main__":
    main()
