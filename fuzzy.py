import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

from settings import Settings


# UTILITY TO COLORIZE TERMINAL
# ================================================================================

class Colors:
    orange = '#f39c12'
    green = '#27ae60'
    blue = '#3498db'
    red = '#e74c3c'
    purple = '#8e44ad'


# INITIALIZE UNIVERSE VARIABLES AND MEMBERSHIP FUNCTIONS
# ================================================================================

def initialize(show_mf: bool = False):
    """
    Initialize Universe Variables and Membership Functions

    Parameters:
    -----------
    show_mf:
         Boolean that controls if the membership function should be shown or not

    Returns:
    --------
    u_variables :
        Universe variables array
    m_functions :
        Membership functions array
    """

    # Generate universe variables
    x_cpu = np.arange(0, 101, 1)
    x_memory = np.arange(0, 101, 1)
    x_disk = np.arange(0, 101, 1)
    x_health = np.arange(0, 101, 1)

    # Generate CPU fuzzy membership functions
    cpu_low = fuzz.trapmf(x_cpu, [0, 0, 50, 60])
    cpu_high = fuzz.trapmf(x_cpu, [50, 60, 90, 95])
    cpu_critical = fuzz.trapmf(x_cpu, [90, 95, 100, 100])

    # Generate MEMORY fuzzy membership functions
    memory_low = fuzz.trapmf(x_memory, [0, 0, 30, 35])
    memory_normal = fuzz.trapmf(x_memory, [30, 35, 60, 70])
    memory_high = fuzz.trapmf(x_memory, [60, 70, 85, 90])
    memory_critical = fuzz.trapmf(x_memory, [85, 90, 100, 100])

    # Generate DISK fuzzy membership functions
    disk_low = fuzz.trapmf(x_disk, [0, 0, 70, 80])
    disk_high = fuzz.trapmf(x_disk, [75, 80, 90, 95])
    disk_critical = fuzz.trapmf(x_disk, [90, 95, 100, 100])

    # Generate output (HEALTH) fuzzy membership functions
    health_normal = fuzz.trapmf(x_health, [0, 0, 50, 60])
    health_degraded = fuzz.trapmf(x_health, [50, 60, 80, 90])
    health_critical = fuzz.trapmf(x_health, [80, 90, 100, 100])

    if show_mf:
        with plt.style.context('bmh'):
            # Visualize these universes and membership functions
            fig, (ax0, ax1, ax2, ax3) = plt.subplots(nrows=4, figsize=(8, 9), num='bmh')

            ax0.plot(x_cpu, cpu_low, Colors.green, linewidth=1.5, label='Normal')
            ax0.plot(x_cpu, cpu_high, Colors.orange, linewidth=1.5, label='High')
            ax0.plot(x_cpu, cpu_critical, Colors.red, linewidth=1.5, label='Critical')
            ax0.set_title('CPU Usage (%)')
            ax0.legend(facecolor="white")

            ax1.plot(x_memory, memory_low, Colors.blue, linewidth=1.5, label='Baixo')
            ax1.plot(x_memory, memory_normal, Colors.green, linewidth=1.5, label='Normal')
            ax1.plot(x_memory, memory_high, Colors.orange, linewidth=1.5, label='High')
            ax1.plot(x_memory, memory_critical, Colors.red, linewidth=1.5, label='Critical')
            ax1.set_title('Memory Usage (%)')
            ax1.legend(facecolor="white")

            ax2.plot(x_disk, disk_low, Colors.green, linewidth=1.5, label='Normal')
            ax2.plot(x_disk, disk_high, Colors.orange, linewidth=1.5, label='High')
            ax2.plot(x_disk, disk_critical, Colors.red, linewidth=1.5, label='Critical')
            ax2.set_title('Disk Usage (%)')
            ax2.legend(facecolor="white")

            ax3.plot(x_health, health_normal, Colors.green, linewidth=1.5, label='Normal')
            ax3.plot(x_health, health_degraded, Colors.orange, linewidth=1.5, label='Degraded')
            ax3.plot(x_health, health_critical, Colors.red, linewidth=1.5, label='Critical')
            ax3.set_title('Healthcheck')
            ax3.legend(facecolor="white")

            # Turn off top/right axes
            for ax in (ax0, ax1, ax2):
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.get_xaxis().tick_bottom()
                ax.get_yaxis().tick_left()

            plt.tight_layout()
            plt.show()

    # Universe Variables
    u_variables = {
        'cpu': x_cpu,
        'memory': x_memory,
        'disk': x_disk,
        'health': x_health
    }

    # Membership functions
    m_functions = {
        'cpu': {
            'low': cpu_low,
            'high': cpu_high,
            'critical': cpu_critical
        },
        'memory': {
            'low': memory_low,
            'normal': memory_normal,
            'high': memory_high,
            'critical': memory_critical
        },
        'disk': {
            'low': disk_low,
            'high': disk_high,
            'critical': disk_critical
        },
        'health': {
            'normal': health_normal,
            'degraded': health_degraded,
            'critical': health_critical
        }
    }

    # Return 2 things:
    #   I.  Universe Variables
    #   II. Membership Functions
    return u_variables, m_functions


def fuzzify(u_variables: dict, m_functions: dict, timestamp: str, cpu_usage: float, memory_usage: float,
            disk_usage: float):
    """
    Fuzzify

    Parameters:
    -----------
        u_variables :
            Universe variables
        m_functions :
            Membership functions
        timestamp :
            Timestamp of last reading
        cpu_usage :
            CPU usage of last reading
        memory_usage :
            Memory usage of last reading
        disk_usage :
            Disk usage of last reading
    """

    # Activate CPU fuzzy membership functions
    cpu_level_low = fuzz.interp_membership(u_variables['cpu'], m_functions['cpu']['low'], cpu_usage)
    cpu_level_high = fuzz.interp_membership(u_variables['cpu'], m_functions['cpu']['high'], cpu_usage)
    cpu_level_critical = fuzz.interp_membership(u_variables['cpu'], m_functions['cpu']['critical'], cpu_usage)

    # Activate MEMORY fuzzy membership functions
    memory_level_low = fuzz.interp_membership(u_variables['memory'], m_functions['memory']['low'], memory_usage)
    memory_level_normal = fuzz.interp_membership(u_variables['memory'], m_functions['memory']['normal'], memory_usage)
    memory_level_high = fuzz.interp_membership(u_variables['memory'], m_functions['memory']['high'], memory_usage)
    memory_level_critical = fuzz.interp_membership(u_variables['memory'], m_functions['memory']['critical'],
                                                   memory_usage)

    # Activate DISK fuzzy membership functions
    disk_level_low = fuzz.interp_membership(u_variables['disk'], m_functions['disk']['low'], disk_usage)
    disk_level_high = fuzz.interp_membership(u_variables['disk'], m_functions['disk']['high'], disk_usage)
    disk_level_critical = fuzz.interp_membership(u_variables['disk'], m_functions['disk']['critical'], disk_usage)

    # RULES:
    #   I.   If CPU is critical or MEMORY is critical is critical or DISK is critical THEN healthcheck is critical
    #   II.  If CPU or MEMORY is high THEN healthcheck is degraded
    #   III. All rest = health is normal

    # Apply Rule 1
    #     IF cpu | memory | disk is critical THEN health is critical
    rule_1 = np.fmax(cpu_level_critical, np.fmax(memory_level_critical, disk_level_critical))

    # Connect Rule 1 with health critical membership function
    health_activation_critical = np.fmin(rule_1, m_functions['health']['critical'])

    # Apply Rule 2
    #     IF cpu | memory is high THEN health is degraded
    rule_2 = np.fmax(cpu_level_high, memory_level_high)

    # Connect Rule 2 with health degraded membership function
    health_activation_degraded = np.fmin(rule_2, m_functions['health']['degraded'])

    # Apply Rule 3
    #     IF cpu is low AND memory is normal AND disk is low THEN health is normal
    rule_3 = np.fmin(cpu_level_low, np.fmin(memory_level_normal, disk_level_low))

    # Connect Rule 3 with health normal membership function
    health_activation_low = np.fmin(rule_3, m_functions['health']['normal'])

    # Create zeroes array
    health_zero = np.zeros_like(u_variables['health'])

    # Aggregate all three output membership functions together
    aggregated = np.fmax(health_activation_critical, np.fmax(health_activation_degraded, health_activation_low))

    try:
        # Calculate defuzzified result
        health = fuzz.defuzz(u_variables['health'], aggregated, 'centroid')
        health_activation = fuzz.interp_membership(u_variables['health'], aggregated, health)

        with plt.style.context('bmh'):
            # Visualize this
            fig, ax0 = plt.subplots(figsize=(8, 3), num='bmh')

            ax0.plot(u_variables['health'], m_functions['health']['normal'], Colors.green, linewidth=1.5, label='Normal')
            ax0.plot(u_variables['health'], m_functions['health']['degraded'], Colors.orange, linewidth=1.5, label='Degraded')
            ax0.plot(u_variables['health'], m_functions['health']['critical'], Colors.red, linewidth=1.5, label='Critical')
            ax0.fill_between(u_variables['health'], health_zero, aggregated, facecolor=Colors.orange, alpha=0.2)
            ax0.plot([health, health], [0, health_activation], Colors.purple, linewidth=1)
            ax0.set_title('Healthcheck time: {}'.format(timestamp))
            ax0.legend(facecolor='white')

            # Turn off top/right axes
            for ax in (ax0,):
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.get_xaxis().tick_bottom()
                ax.get_yaxis().tick_left()

            # Show plot
            plt.tight_layout()
            plt.show(block=False)
            plt.pause(Settings.PLOT_PERIOD_IN_SECONDS)
            plt.close()

    except Exception:
        pass


if __name__ == '__main__':
    # Initialize
    universe_variables, membership_functions = initialize(show_mf=True)

    while True:
        with open('output.txt', 'r') as f:
            # Read from file and close it
            last_reading = f.readlines()[-1].replace('\n', '').split(';')
            f.close()

        # Read from file
        timestmp = last_reading[0]
        disk = float(last_reading[1])
        memory = float(last_reading[2])
        cpu = float(last_reading[3])

        fuzzify(universe_variables, membership_functions, timestmp, cpu, memory, disk)
