# Logger
import os

def init_storage(output_folder, log_file):
    os.makedirs(output_folder, exist_ok=True)

    if not os.path.exists(log_file):
        with open(log_file, "w") as f:
            f.write("Timestamp,Image,Class,Confidence\n")
    
    performance_log = "performance_log.txt"

    if not os.path.exists(performance_log):
        with open(performance_log, "w") as f:
            f.write("Timestamp,Latency,CPU,RAM\n")


def log_to_file(log_file, timestamp, filename, label, confidence):
    with open(log_file, "a") as f:
        f.write(f"{timestamp},{filename},{label},{confidence:.2f}\n")


def log_performance(log_file, timestamp, latency, cpu, ram):
    with open(log_file, "a") as f:
        f.write(f"{timestamp},{latency:.2f},{cpu:.2f},{ram:.2f}\n")