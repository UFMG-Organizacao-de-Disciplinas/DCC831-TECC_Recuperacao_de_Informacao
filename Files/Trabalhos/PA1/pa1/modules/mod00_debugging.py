
import json
import time # Time functions
from requests.structures import CaseInsensitiveDict
import threading # For multithreading

""" print_json: Pretty print JSON data """

def print_json(data):
    """ Pretty prints JSON data. """
    def convert(obj):
        if isinstance(obj, set):
            return list(obj)
        if isinstance(obj, CaseInsensitiveDict):
            return dict(obj)
        raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')

    print(json.dumps(data, indent=4, default=convert))


""" benchmarking """

def benchmark_test(function, parameters):
    """ Benchmarking function to measure execution time. """
    start_time = time.time()
    result = function(*parameters)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(
        f"Function {function.__name__} executed in {elapsed_time:.4f} seconds")
    return result

# benchmark_test(get_robots_txt, ['https://olhardigital.com.br'])
# benchmark_test(get_sitemap, ['https://olhardigital.com.br', {'sitemap': []}])


""" debug_print: Prints the parsed URL in a readable format that is defined in the assignment. """

def debug_print(parsed_url):
    """ Prints the parsed URL in a readable format. """
    debug_info = {
        'URL': parsed_url['URL'],
        'Title': parsed_url['Title'],
        'Text': parsed_url['Text'],
        'Timestamp': parsed_url['Timestamp'],
    }
    print_json(debug_info)


def debug_scrape_print(scraping, url, active_threads=None):
    """ Prints the scraping state. """
    msg = f'({scraping["count"]:04}/{len(scraping["frontier"]):04})\t'
    msg += url
    msg += f'\t[Threads: {threading.active_count()}]'
    # msg += f' => {PAGES_LIMIT}'
    # first_3_plus_last_3 = list(scraping['frontier'])[:2] + list(scraping['frontier'])[-2:]
    # msg += f'\nFrontier: {first_3_plus_last_3}'
    # msg_debug_repeat = f'({scraping["count"]}): 
    print(msg)
    # print_json(scraping)
    # if scraping['count'] % 100 == 0:  # Print status every 100 iterations