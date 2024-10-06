import os
import sys
import csv
import time
import psutil
from utils import generate_timestamped_filename


class ProcessMonitor:
    def __init__(self, process_dict, interval=5, config=None):
        if config is None:
            print("A valid Config instance must be provided.")
            sys.exit(1)

        self.config = config
        self.output_file = self.init_output_file()

        self.process_dict = process_dict
        self.interval = interval

    def init_output_file(self):
        if self.config.data_format == 'csv':
            csv_file = generate_timestamped_filename("process", self.config.data_format)
            csv_path = os.path.join(self.config.directory, csv_file)
            with open(file=csv_path, mode='w+', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Process Name', 'PID', 'CPU %', 'Memory %', 'Memory'])
            return csv_path

    def get_resource_usage(self):
        for pid, process_name in self.process_dict.items():
            process = psutil.Process(pid)
            self.save_to_csv(process_name, pid, process.cpu_percent(self.interval),
                             process.memory_percent(), process.memory_info().rss / (1024 * 1024))

    def save_to_csv(self, process_name, pid, cpu_percent, memory_percent, memory):
        with open(file=self.output_file, mode='a+', newline='') as csv_file:
            writer = csv.writer(csv_file)
            cpu_percent = round(cpu_percent, 2)
            memory_percent = round(memory_percent, 2)
            memory = round(memory, 2)

            writer.writerow([process_name, pid, cpu_percent, memory_percent, memory])

    def start_monitoring(self):
        while True:
            self.get_resource_usage()
            time.sleep(self.interval)
