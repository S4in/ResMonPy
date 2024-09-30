import argparse
import ctypes
import sys
from config import Config
from network import NetworkMonitor
from utils import is_admin, parse_arguments


def main():
    # Check if the script is running with administrator privileges
    if not is_admin():
        print("This script requires administrator privileges. Please run as an administrator.")
        sys.exit(1)

    args = parse_arguments()

    # Set up the config with the user-provided or default log directory
    config = Config(log_dir=args.log_dir)

    # Initialize the NetworkMonitor with the passed arguments and config
    network_monitor = NetworkMonitor(process_names=args.processes, interval=args.interval, config=config)
    network_monitor.start_monitoring()


if __name__ == "__main__":
    main()
