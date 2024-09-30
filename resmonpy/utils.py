import ctypes
import argparse


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
        default="C:\\Temp\\monitor_logs",  # Default log directory
        help="Directory where log files will be stored (default: C:\\Temp\\monitor_logs)"
    )

    return parser.parse_args()
