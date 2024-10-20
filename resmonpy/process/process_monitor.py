import os
import sys
import csv

import time
import psutil
from datetime import datetime
from threading import Thread, Event, Lock
from resmonpy.utils import generate_timestamped_filename
from resmonpy.process import get_pid


class ProcessMonitor:
    def __init__(self, process_dict, interval, config=None):
        if config is None:
            print("A valid Config instance must be provided.")
            sys.exit(1)

        self.config = config
        self.output_file = self.init_output_file()

        self.process_dict = process_dict
        self.interval = interval
        self.event = Event()
        self.lock = Lock()

    def init_output_file(self):
        if self.config.data_format == 'csv':
            csv_file = generate_timestamped_filename("process", self.config.data_format)
            csv_path = os.path.join(self.config.directory, csv_file)
            with open(file=csv_path, mode='w+', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Time', 'Process Name', 'PID', 'CPU %', 'Memory %', 'Memory'])

            return csv_path

    def get_resource_usage(self):
        with self.lock:
            for pid, process_name in self.process_dict.items():

                if psutil.pid_exists(pid):
                    process = psutil.Process(pid)
                    self.save_to_csv(process_name, pid, process.cpu_percent(),
                                     process.memory_percent(), process.memory_info().rss / (1024 * 1024))

    def save_to_csv(self, process_name, pid, cpu_percent, memory_percent, memory):
        with open(file=self.output_file, mode='a+', newline='') as csv_file:
            writer = csv.writer(csv_file)
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            cpu_percent = round(cpu_percent, 2)
            memory_percent = round(memory_percent, 2)
            memory = round(memory, 2)
            writer.writerow([dt_string, process_name, pid, cpu_percent, memory_percent, memory])

    def update(self):
        with self.lock:
            self.process_dict = get_pid(list(self.process_dict.values()))
            if not self.process_dict:
                self.stop()

    def run_updates(self):
        while not self.event.is_set():
            time.sleep(self.interval * 10)
            self.update()

    def monitor_usage(self):
        while not self.event.is_set():
            self.get_resource_usage()
            time.sleep(self.interval)

    def start_monitoring(self):
        monitor_thread = Thread(target=self.monitor_usage)
        update_thread = Thread(target=self.run_updates)
        update_thread.daemon = True
        try:
            monitor_thread.start()
            update_thread.start()
            while not self.event.is_set():
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.stop()
            print("Process monitoring aborted by user")
            monitor_thread.join()

    def stop(self):
        self.event.set()
