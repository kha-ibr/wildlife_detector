# Logger
import os

def init_storage(output_folder, log_file):
    os.makedirs(output_folder, exist_ok=True)

    if not os.path.exists(log_file):
        with open(log_file, "w") as f:
            f.write("Timestamp,Image,Class,Confidence\n")


def log_to_file(log_file, timestamp, filename, label, confidence):
    with open(log_file, "a") as f:
        f.write(f"{timestamp},{filename},{label},{confidence:.2f}\n")