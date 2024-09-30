import psutil
import time
import sys
from scapy.all import sniff
from scapy.layers.inet import TCP, UDP
from datetime import datetime
import threading
from collections import deque
from config import Config


class NetworkMonitor:
    def __init__(self, process_names, interval=1, config=None):
        self.netstat_data = []
        self.pid_list = []
        self.monitor_ports = []

        if config is None:
            raise ValueError("A valid Config instance must be provided.")

        self.config = config

        self.lock = threading.Lock()

        self.interval = interval
        self.total_sent = 0
        self.total_received = 0
        self.previous_sent = 0
        self.previous_received = 0
        self.sent_history = deque(maxlen=60)
        self.received_history = deque(maxlen=60)

        for process_name in process_names:
            self.get_pid(process_name=process_name)

        self.refresh_ports()

        if not self.monitor_ports:
            log_message = (f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - No ports to monitor for the given "
                           f"processes.")
            print(log_message)
            self.config.logger.info(log_message)  # Use the logger from the Config instance
            sys.exit(1)

    def get_network_statistic(self):
        connections = psutil.net_connections(kind='inet')
        self.netstat_data = []
        for conn in connections:
            conn_data = {
                "local_port": f"{conn.laddr.port}" if conn.laddr else "N/A",
                "status": conn.status,
                "pid": conn.pid if conn.pid else "N/A"
            }
            self.netstat_data.append(conn_data)

    def get_pid(self, process_name):
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'] == process_name:
                    self.pid_list.append(proc.info['pid'])
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

    def filter_ports(self, pid):
        ports = [conn["local_port"] for conn in self.netstat_data if conn['pid'] == pid]
        for port in ports:
            if port not in self.monitor_ports:
                self.monitor_ports.append(port)

    def refresh_ports(self):
        with self.lock:
            self.get_network_statistic()
            self.monitor_ports.clear()
            for pid in self.pid_list:
                self.filter_ports(pid)

    def packet_callback(self, packet):
        if packet.haslayer(TCP) or packet.haslayer(UDP):
            if packet.haslayer(TCP):
                sport = packet[TCP].sport
                dport = packet[TCP].dport
            elif packet.haslayer(UDP):
                sport = packet[UDP].sport
                dport = packet[UDP].dport

            with self.lock:
                if sport in self.monitor_ports:
                    self.total_sent += len(packet)
                if dport in self.monitor_ports:
                    self.total_received += len(packet)

    def calculate_average_bps(self):
        while True:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            with self.lock:
                total_sent_diff = self.total_sent - self.previous_sent
                total_received_diff = self.total_received - self.previous_received

                self.previous_sent = self.total_sent
                self.previous_received = self.total_received

                self.sent_history.append(total_sent_diff)
                self.received_history.append(total_received_diff)

            avg_sent_bps = sum(self.sent_history) / len(self.sent_history)
            avg_received_bps = sum(self.received_history) / len(self.received_history)

            log_message = f"Average Sent: {avg_sent_bps:.2f} B/s, Average Received: {avg_received_bps:.2f} B/s"
            print(f"{timestamp} - {log_message}")
            self.config.logger.info(log_message)  # Use the logger from the Config instance

            time.sleep(self.interval)

    def start_sniffing(self):
        port_filter = " or ".join([f"tcp port {port} or udp port {port}" for port in self.monitor_ports])

        sniff_thread = threading.Thread(target=sniff, kwargs={
            'filter': port_filter, 'prn': self.packet_callback, 'store': 0})
        sniff_thread.daemon = True
        sniff_thread.start()

    def refresh_ports_thread(self):
        while True:
            self.refresh_ports()
            time.sleep(self.interval)

    def start_monitoring(self):
        refresh_thread = threading.Thread(target=self.refresh_ports_thread)
        refresh_thread.daemon = True
        refresh_thread.start()

        self.start_sniffing()
        self.calculate_average_bps()
