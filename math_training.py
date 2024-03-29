#!/usr/bin/env python3

import bisect
import collections
import datetime
import json
import os
import random
import time
import termcolor


QUESTION_COUNT = 10
RESULTS_DIR = 'results'


Question = collections.namedtuple(
    'Question', ['first', 'second', 'operation', 'expected'])


Result = collections.namedtuple(
    'Result', ['question', 'error_count', 'time_sec'])


def make_question():
    a = random.randint(100, 999)
    b = random.randint(100, 999)
    operation = '+' if random.randint(0, 1) == 0 else '-'
    if operation == '+':
        expected = a + b
    else:
        expected = a - b
    return Question(a, b, operation, expected)


def ask_question(question):
    start_time = time.time()
    error_count = 0
    while True:
        print('{} {} {} = ... '.format(
            question.first, question.operation, question.second))
        try:
            result = input()
            result = int(result)
        except ValueError:
            print(f'Not a number {result}. Try again')
            continue
        if result == question.expected:
            break
        print(termcolor.colored('WRONG!', 'red'))
        error_count += 1
    time_delta = time.time() - start_time
    return Result(question, error_count, time_delta)


def result_file_name():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    d = datetime.datetime.fromtimestamp(time.time())
    file_name = d.strftime('%Y-%m-%d_%H-%M-%S.json')
    return os.path.join(script_dir, RESULTS_DIR, file_name)


def results_to_dicts(items):
    result = []
    for item in items:
        d = item._asdict()
        d['question'] = item.question._asdict()
        result.append(d)
    return result


def save_results(results):
    file_name = result_file_name()
    dir_name = os.path.dirname(file_name)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    with open(file_name, 'w') as f:
        json.dump(results_to_dicts(results), f)

def load_all_times():
    result = []
    for file_name in os.listdir(RESULTS_DIR):
        date_str = file_name.split('.')[0]
        if not date_str:
            continue
        with open(os.path.join(RESULTS_DIR, file_name), 'r') as f:
            items = json.load(f)
        total_time = sum(d['time_sec'] for d in items)
        result.append(total_time)
    return result

def main():
    results = []
    all_times = load_all_times()
    start = time.time()
    error_count = 0
    for question_idx in range(1, QUESTION_COUNT + 1):
        print(termcolor.colored(
            '# {}:'.format(question_idx),
            'blue'))
        question = make_question()
        result = ask_question(question)
        error_count += result.error_count
        results.append(result)
    time_delta = time.time() - start
    save_results(results)
    all_times.sort()
    this_place = bisect.bisect_left(all_times, time_delta)
    print(termcolor.colored(
        f'{QUESTION_COUNT} operations took {time_delta:.3f} sec. {error_count} errors.',
        'green'))
    print(termcolor.colored(
        f'This is {this_place + 1} place (by time) among {len(all_times) + 1}',
        'green'))
    percentile = ((this_place + 1) * 100.) / (len(all_times) + 1)
    print(termcolor.colored(
        f'This result is in the top {percentile:.3f}%',
        'green'))


if __name__ == '__main__':
    main()
