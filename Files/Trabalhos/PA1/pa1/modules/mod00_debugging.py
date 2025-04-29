""" Debugging functions to assist in the development of the web scraper """

# Importing my needed libraries

import json
import time # Time functions
from requests.structures import CaseInsensitiveDict
import threading # For multithreading

# Global variables

start_time = time.time()  # Start time for the entire script
partial_time = time.time()  # Start time for the partial checkpoint

# Debugging functions

def print_json(data):
    """ Pretty prints JSON data. """
    def convert(obj):
        if isinstance(obj, set):
            return list(obj)
        if isinstance(obj, CaseInsensitiveDict):
            return dict(obj)
        raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')

    print(json.dumps(data, indent=4, default=convert))

def benchmark_test(function, parameters):
    """ Benchmarking function to measure execution time. """
    start_time = time.time()
    result = function(*parameters)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(
        f"Function {function.__name__} executed in {elapsed_time:.4f} seconds")
    return result

def debug_scrape_print(scraping, url, active_threads=None):
    """ Prints the scraping state. """
    scraping_count = f'({scraping['count']:04}/{len(scraping['frontier']):04})\t'
    thread_count = f'[Threads: {threading.active_count():02}]'
    storage_count = f'[Stored: {scraping['stored']:03}]'

    msg = ''
    msg += f'{storage_count}\t'
    # msg += f'{thread_count}\t'
    msg += f'{scraping_count}\t'
    # msg += f'{url}'
    
    # msg += f' => {PAGES_LIMIT}'
    # first_3_plus_last_3 = list(scraping['frontier'])[:2] + list(scraping['frontier'])[-2:]
    # msg += f'\nFrontier: {first_3_plus_last_3}'
    # msg_debug_repeat = f'({scraping["count"]}): 
    print(msg)
    # print_json(scraping)
    # if scraping['count'] % 100 == 0:  # Print status every 100 iterations

def debug_time_elapsed():
    """ Returns the time elapsed since the start time """
    global start_time, partial_time
    end_time = time.time()
    
    from_last_checkpoint = end_time - partial_time
    from_start = end_time - start_time
    
    msg = f'TIMES: from start: {from_start:.2f} seconds\tfrom last save: {from_last_checkpoint:2f} seconds'
    print(msg)
    
    partial_time = end_time  # Update the checkpoint time

