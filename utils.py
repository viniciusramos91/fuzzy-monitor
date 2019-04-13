import random
from datetime import datetime
from termcolor import colored
import psutil

from settings import Settings


def format_timestamp(timestamp):
    return colored('[{:>8}]'.format(timestamp), 'yellow')


def format_disk_usage(disk_usage, disk_usage_threshold):
    if disk_usage < disk_usage_threshold:
        color = 'blue'
    else:
        color = 'red'

    return colored('{:>16}'.format(str(disk_usage)), color)


def format_memory_usage(memory_usage, memory_usage_threshold):
    if memory_usage < memory_usage_threshold:
        color = 'blue'
    else:
        color = 'red'

    return colored('{:>15}'.format(str(memory_usage)), color)


def format_cpu_usage(cpu_usage, cpu_usage_threshold):
    if cpu_usage < cpu_usage_threshold:
        color = 'blue'
    else:
        color = 'red'

    return colored('{:>11}'.format(str(cpu_usage)), color)


def format_header():
    headers = '{:->52}\n'.format('') + \
              '{:>10}'.format('TIMESTAMP') + \
              '{:>16}'.format('DISK (%)') + \
              '{:>15}'.format('MEMORY (%)') + \
              '{:>11}'.format('CPU (%)') + \
              '\n{:->52}'.format('')

    print(colored(headers, 'magenta'))


def format_data(disk_usage_threshold, memory_usage_threshold, cpu_usage_threshold):
    timestamp = str(datetime.now().strftime('%H:%M:%S'))
    disk_usage = random.randint(40, 100) if Settings.DUMMY_DISK_USAGE else psutil.disk_usage('C:').percent
    memory_usage = psutil.virtual_memory().percent
    cpu_usage = psutil.cpu_percent()

    print(
        timestamp +
        format_disk_usage(disk_usage, disk_usage_threshold) +
        format_memory_usage(memory_usage, memory_usage_threshold) +
        format_cpu_usage(cpu_usage, cpu_usage_threshold)
    )

    return timestamp, disk_usage, memory_usage, cpu_usage


def save_to_file(timestamp, disk_usage, memory_usage, cpu_usage):
    with open('output.txt', 'a') as f:
        f.write(
            '{};{};{};{}\n'.format(timestamp, disk_usage, memory_usage, cpu_usage)
        )

        f.close()
