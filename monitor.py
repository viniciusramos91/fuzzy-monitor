from settings import Settings
from utils import format_data, save_to_file, format_header
from time import sleep

# MONITOR PROCESS TO GATHER COMPUTER RESOURCES (MEMORY, DISK AND ACPU)
# ===========================================================================================

if __name__ == '__main__':
    counter = 0

    f = open('output.txt', 'w')
    f.write('TIMESTAMP;DISK;MEMORY;CPU\n')
    f.close()

    format_header()

    while True:
        timestamp, disk_usage, memory_usage, cpu_usage = format_data(
            disk_usage_threshold=Settings.DISK_USAGE_THRESHOLD,
            memory_usage_threshold=Settings.MEMORY_USAGE_THRESHOLD,
            cpu_usage_threshold=Settings.CPU_USAGE_THRESHOLD
        )

        counter += 1

        if counter >= 10:
            save_to_file(timestamp, disk_usage, memory_usage, cpu_usage)

        sleep(Settings.MONITORING_PERIOD_IN_SECONDS)
