import os
from datetime import datetime


def generate_timestamped_file(data_category,data_format):
    """Generate a log file name with a timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{data_category}_{timestamp}.{format}"


class Config:
    def __init__(self, log_dir="C:\\Temp\\resmonpy", data_format="csv", data_category="network"):
        self.log_dir = log_dir
        self.log_file = generate_timestamped_file(data_category, data_format)
        self.data_file = generate_timestamped_file(data_category, "log")  # Generate the log file with a timestamp
        self.verify_log_dir()

    def verify_log_dir(self):
        """Ensure that the Temp and logs directories exist. If not, create them."""
        temp_dir = os.path.dirname(self.log_dir)

        # Create Temp directory if it doesn't exist
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        # Create the resmonpy directory if it doesn't exist
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def get_log_path(self):
        """Return the full path to the log file."""
        return os.path.join(self.log_dir, self.log_file)
