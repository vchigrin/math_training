#!/usr/bin/env python3

import datetime
import json
import matplotlib.pyplot as plt
import os
from math_training import RESULTS_DIR

def load_data():
    result = {}
    for file_name in os.listdir(RESULTS_DIR):
        date_str = file_name.split('.')[0]
        if not date_str:
            continue
        dt = datetime.datetime.strptime(date_str, '%Y-%m-%d_%H-%M-%S')
        with open(os.path.join(RESULTS_DIR, file_name), 'r') as f:
            items = json.load(f)
        total_time = sum(d['time_sec'] for d in items)
        total_errors = sum(d['error_count'] for d in items)
        result[dt] = {'time_sec': total_time, 'error_count': total_errors}
    return result


def main():
    dates_to_times = load_data()
    fix, (time_ax, err_ax) = plt.subplots(2, 1)
    time_ax.set_title('Total test time')
    time_ax.scatter(dates_to_times.keys(),
                [d['time_sec'] for d in dates_to_times.values()],
                marker='+', c='r')
    err_ax.set_title('Total errors count')
    err_ax.scatter(dates_to_times.keys(),
                [d['error_count'] for d in dates_to_times.values()],
                marker='+', c='r')
    plt.show()

if __name__ == '__main__':
    main()
