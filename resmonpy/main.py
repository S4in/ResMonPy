import argparse
import ctypes
import sys
import threading
from config import Config
from network import NetworkMonitor
from process import ProcessMonitor
from process import get_pid
from utils import is_admin, parse_arguments, verify_processes
import time
import multiprocessing


def run_process(class_instance):
    class_instance.start_monitoring()


def main():
    if not is_admin():
        print("This script requires administrator privileges. Please run as an administrator.")
        sys.exit(1)

    args = parse_arguments()
    config = Config(directory=args.directory)
    process_names = verify_processes(args.processes)
    process_dict = get_pid(process_names)

    if args.monitor == 'network':
        network_monitor = NetworkMonitor(process_dict=process_dict, interval=args.interval, config=config)
        network_monitor.start_monitoring()
    elif args.monitor == 'process':
        process_monitor = ProcessMonitor(process_dict=process_dict, interval=args.interval, config=config)
        process_monitor.start_monitoring()

    elif args.monitor == 'all':
        network_monitor = NetworkMonitor(process_dict=process_dict, interval=args.interval, config=config)
        process_monitor = ProcessMonitor(process_dict=process_dict, interval=args.interval, config=config)

        try:
            process_thread = threading.Thread(target=process_monitor.start_monitoring)
            process_thread.daemon = True
            process_thread.start()
            network_monitor.start_monitoring()

            process_thread.join()

        except KeyboardInterrupt:
            process_monitor.stop()
            network_monitor.stop()
            print("Network monitor aborted by user")
            sys.exit(0)
        except Exception as ex:
            process_monitor.stop()
            network_monitor.stop()
            print(f"Error occurred while monitoring network and processes: {ex}")
            sys.exit(1)


if __name__ == "__main__":
    main()
