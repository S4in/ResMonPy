import os
import logging
from datetime import datetime

class Config:
    def __init__(self, log_dir="C:\\Temp\\monitor_logs", log_file_prefix="network_log"):
        self.log_dir = log_dir
        self.log_file_prefix = log_file_prefix
        self.logger = None
        self.log_file = self.generate_timestamped_log_file()  # Generate the log file with a timestamp
        self.ensure_log_directory_exists()
        self.setup_logging()

    def generate_timestamped_log_file(self):
        """Generate a log file name with a timestamp."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{self.log_file_prefix}_{timestamp}.log"

    def ensure_log_directory_exists(self):
        """Ensure that the Temp and logs directories exist. If not, create them."""
        temp_dir = os.path.dirname(self.log_dir)

        # Create Temp directory if it doesn't exist
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
            print(f"Created temp directory: {temp_dir}")

        # Create the monitor_logs directory if it doesn't exist
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
            print(f"Created log directory: {self.log_dir}")

    def setup_logging(self):
        """Set up logging with the given log directory and file."""
        log_path = os.path.join(self.log_dir, self.log_file)

        # Set up logging
        logging.basicConfig(
            filename=log_path,
            level=logging.INFO,
            format="%(asctime)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Create the logger instance
        self.logger = logging.getLogger()

        # Log a message indicating that logging has started
        self.logger.info(f"Logging started in {log_path}")

    def get_log_path(self):
        """Return the full path to the log file."""
        return os.path.join(self.log_dir, self.log_file)
