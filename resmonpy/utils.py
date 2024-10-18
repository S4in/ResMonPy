import ctypes
import argparse
from datetime import datetime


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except (AttributeError, OSError) as ex:
        return False


def parse_arguments():
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
        default=5,
        required=False,
        help="Interval in seconds (default: 5 seconds)"
    )

    parser.add_argument(
        "-d", "--directory",
        type=str,
        default="C:\\Temp\\resmonpy",
        required=False,
        help="Directory where output files will be stored (default: C:\\Temp\\resmonpy)"
    )
    parser.add_argument(
        "-f", "--format",
        choices=['csv', 'json'],
        default='csv',
        required=False,
        help="Format for output files (default: csv, options: csv, json)"
    )

    parser.add_argument(
        "-m", "--monitor",
        type=str,
        choices=['process', 'network', 'all'],
        default="all",
        required=False,
        help="Select type of a monitor (default: all, options: process, network, all)"
    )
    
    return parser.parse_args()


def verify_extension(process_name):
    if not process_name.lower().endswith('.exe'):
        return process_name + '.exe'
    return process_name


def verify_processes(process_list):
    verified_processes = []
    for proces_name in process_list:
        verified_processes.append(
            verify_extension(proces_name)
        )
    return verified_processes


def generate_timestamped_filename(data_category,data_format):
    """Generate a log file name with a timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{data_category}_{timestamp}.{data_format}"
