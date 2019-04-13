"""
Produces load on available CPU cores
"""

from multiprocessing import Pool
from multiprocessing import cpu_count


def load_cpu(x):
    while True:
        x * x


if __name__ == '__main__':
    # Get number or CPUs
    processes = cpu_count()

    if processes > 1:
        print('Using %d cores\n' % (processes-1))

        # Create a pool on 'processes-1' cores
        pool = Pool(processes)
        pool.map(load_cpu, range(processes))
    else:
        print('Using %d cores\n' % processes)

        # Create a pool on 'processes' cores
        pool = Pool(processes)
        pool.map(load_cpu, range(processes))
