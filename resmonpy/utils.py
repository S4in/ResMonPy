import sys
from collections import defaultdict
import psutil
import ctypes
import argparse


def get_pid(process_name):
    pid = None
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'] == process_name:
                pid = proc.info['pid']
            else:
                print(F"Process: {process_name} was not found")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return pid


def verify_extension(process_name):
    if not process_name.lower().endswith('.exe'):
        return process_name + '.exe'
    return process_name


def match_pid(processes):
    process_dict = defaultdict(str)
    for process_name in processes:
        process_name = verify_extension(process_name=process_name)
        pid = get_pid(process_name=process_name)
        if pid:
            process_dict[pid] = process_name
    return process_dict


def is_admin():
    """Check if the script is being run with administrator privileges on Windows."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def parse_arguments():
    """Parse command-line arguments."""
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
        default="C:\\Temp\\resmonpy",  # Default log directory
        help="Directory where log files will be stored (default: C:\\Temp\\resmonpy)"
    )

    return parser.parse_args()