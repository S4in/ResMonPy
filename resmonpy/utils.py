import ctypes
import argparse
from datetime import datetime


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
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
        default=1,
        help="Interval in seconds (default: 1s)"
    )

    parser.add_argument(
        "-d", "--directory",
        type=str,
        default="C:\\Temp\\resmonpy",  # Default log directory
        help="Directory where output files will be stored (default: C:\\Temp\\resmonpy)"
    )
    parser.add_argument(
        "-f", "--format",
        choices=['csv', 'json'],  # Specify the possible output formats
        default='csv',  # Set the default format to csv
        help="Format for output files (default: csv, options: csv, json)"
    )

    parser.add_argument(
        "-t", "--type",
        type=str,
        default="both",
        required=False,
        help="Monitor network/process/both. Default is both"
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
