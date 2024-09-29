import argparse
import ctypes
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.config import Config
from network.monitor import NetworkMonitor


def is_admin():
    """Check if the script is being run with administrator privileges on Windows."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def main():
    # Check if the script is running with administrator privileges
    if not is_admin():
        print("This script requires administrator privileges. Please run as an administrator.")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Network Monitor for Processes")
    
    parser.add_argument(
        "-p", "--processes", 
        nargs='+', 
        required=True, 
        help="List of process names to monitor"
    )
    
    parser.add_argument(
        "-i", "--interval", 
        type=int, 
        default=1, 
        help="Interval in seconds between average Bps calculations (default: 1s)"
    )

    parser.add_argument(
        "-l", "--log_dir", 
        type=str, 
        default="C:\\Temp\\monitor_logs",  # Default log directory
        help="Directory where log files will be stored (default: C:\\Temp\\monitor_logs)"
    )

    args = parser.parse_args()
    
    # Setup the config with the user-provided or default log directory
    config = Config(log_dir=args.log_dir)

    # Initialize the NetworkMonitor with the passed arguments and config
    network_monitor = NetworkMonitor(process_names=args.processes, interval=args.interval, config=config)
    network_monitor.start_monitoring()


if __name__ == "__main__":
    main()
