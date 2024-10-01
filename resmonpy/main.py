import argparse
import ctypes
import sys
from config import Config
from network import NetworkMonitor
from utils import is_admin, parse_arguments, match_pid


def main():
    if not is_admin():
        print("This script requires administrator privileges. Please run as an administrator.")
        sys.exit(1)

    args = parse_arguments()

    config = Config(log_dir=args.log_dir)
    process_dict = match_pid(args.processes)

    network_monitor = NetworkMonitor(process_dict=process_dict, interval=args.interval, config=config)
    network_monitor.start_monitoring()


if __name__ == "__main__":
    main()
