""" WEB Scraper """

# """ Importando meus módulos """

from modules.mod00_debugging import print_json, benchmark_test, debug_scrape_print # Debugging and benchmarking functions
from modules.mod01_argparse import get_args # Parsing command line arguments
from modules.modXX_WARC_handling import store_warcs # WARC file handling functions
from modules.mod02_utils import constants, get_seeds, get_timestamp, default_requester, get_base_url # HTTP request handling functions
from modules.modXX_frontier import update_frontier # Frontier management functions
# from modules.mod02_utils import  # Constants for the script

# """ Importando as bibliotecas necessárias """

# import beautifulsoup4 as bs
# import certifi                          # Root certificates for validating SSL/TLS (used by requests)
# import charset_normalizer               # Used for detecting and normalizing text encodings (dependency of requests)
# import idna                             # Internationalized domain name support (dependency of requests)
# from protego import Protego             # Parses and enforces robots.txt rules
import requests                         # HTTP library for making requests to web resources
# import six                              # Compatibility layer for writing Python 2/3 code (used by many older libs)
# import soupsieve                        # CSS selector engine for BeautifulSoup
# import typing_extensions                # Adds backported or experimental typing features for older Python versions
# from url_normalize import url_normalize # Normalizes URLs into a consistent format
# import urllib3                          # Low-level HTTP library used by requests
# import warcio                           # Library for reading and writing WARC (Web ARChive) files
# from warcio.capture_http import capture_http # Capture HTTP requests and responses for archiving

# JV
import sys
import time # Time functions
from concurrent.futures import ThreadPoolExecutor, as_completed # For multithreading
import os
from concurrent.futures import wait, FIRST_COMPLETED

# Adicionar no início do script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

start_time = time.time()  # Start time for the entire script

partial_time = time.time()  # Start time for the partial checkpoint

CONSTANTS = constants()
ARGS = get_args(CONSTANTS)

# print(f"Arguments: {ARGS}")  # Debugging line to check the arguments passed to the script

""" Code constants: SEEDS_FILE, PAGES_LIMIT, DEBUG_MODE, MIN_DELAY, MAX_THREADS """

SEEDS_FILE = ARGS.seeds if ARGS.seeds else CONSTANTS['SEEDS_PATH']
PAGES_LIMIT = ARGS.limit if ARGS.limit else CONSTANTS['CORPUS_SIZE']
DEBUG_MODE = ARGS.debug if ARGS.debug else CONSTANTS['DEBUG_MODE']

MAX_THREADS = CONSTANTS['MAX_THREADS'] # Maximum number of threads to use for crawling
MIN_DELAY = CONSTANTS['MIN_DELAY'] # Delay in milliseconds between requests
WARC_SIZE = CONSTANTS['WARC_SIZE'] # Number of pages to write to a WARC file before creating a new one


def debug_time_elapsed():
    """ Returns the time elapsed since the start time """
    global start_time, partial_time
    end_time = time.time()
    
    from_last_checkpoint = end_time - partial_time
    from_start = end_time - start_time
    
    msg = f'TIMES: from start: {from_start:.2f} seconds\tfrom last save: {from_last_checkpoint:2f} seconds'
    print(msg)
    
    partial_time = end_time  # Update the checkpoint time


""" Scraping storage structure """

scraping = {
    'count': 0,
    'stored': 0,
    'content': dict(),
    'stored_urls': set(),  # Set of URLs already stored in WARC
    'frontier': get_seeds(SEEDS_FILE),  # Set of URLs to scrape
}

""" Actual Scraping """



parallel_scrape(scrape_once, scraping, MAX_THREADS)

print(f"Total execution time: {time.time() - start_time:.2f} seconds")