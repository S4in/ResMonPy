import argparse
import ctypes
import sys
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
    
    if args.type == 'network':
        network_monitor = NetworkMonitor(process_dict=process_dict, interval=args.interval, config=config)
        network_monitor.start_monitoring()
    elif args.type == 'process':
        process_monitor = ProcessMonitor(process_dict=process_dict, interval=args.interval, config=config)
        process_monitor.start_monitoring()
    elif args.type == 'both':
        network_monitor = NetworkMonitor(process_dict=process_dict, interval=args.interval, config=config)
        process_monitor = ProcessMonitor(process_dict=process_dict, interval=args.interval, config=config)
        try:
            process1 = multiprocessing.Process(target=run_process, args=(network_monitor,), name="NetworkMonitor")
            process2 = multiprocessing.Process(target=run_process, args=(process_monitor,), name="ProcessMonitor")
            process1.start()
            process2.start()
            process1.join()
            process2.join()
        except KeyboardInterrupt:
            process1.terminate()
            process2.terminate()
            process1.join()
            process2.join()
        except Exception as ex:
            process1.terminate()
            process2.terminate()
            process1.join()
            process2.join()
            print(str(ex))
    else:
        print("Invalid monitoring type. Select from network/process/both")
        sys.exit(1)
if __name__ == "__main__":
    main()
