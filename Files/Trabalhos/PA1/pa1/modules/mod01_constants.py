""" Code constants: SEEDS_FILE, PAGES_LIMIT, DEBUG_MODE, MIN_DELAY, MAX_THREADS """

# Importing my needed libraries

import argparse # Parsing command line arguments

# Global variables

DEFAULT_PATH = '../Seeds/seeds-2024711370.txt'
DEFAULT_LIMIT = 100000

# Constants and parsing argument functions

def constants():
    """ Returns the constants used in the script. """

    local_constants = {
        'MIN_DELAY': 100,  # Minimum delay between requests in miliseconds
        'MAX_DELAY': 5,  # Maximum delay between requests in seconds
        'MAX_RETRIES': 3,  # Maximum number of retries for a request
        'MAX_THREADS': 60,  # Maximum number of threads to use for crawling
        'WARC_SIZE': 100,  # Number of pages to write to a WARC file before creating a new one
        'CORPUS_SIZE': DEFAULT_LIMIT,  # Number of pages to crawl before stopping
        'SEEDS_PATH': DEFAULT_PATH,  # Path to the seed file
        'DEBUG_MODE': False,  # Enable debug mode
    }
    args = get_args()

    local_constants['SEEDS_PATH'] = args.seeds if args.seeds else local_constants['SEEDS_PATH']
    local_constants['CORPUS_SIZE'] = args.limit if args.limit else local_constants['CORPUS_SIZE']
    local_constants['DEBUG_MODE'] = args.debug if args.debug else local_constants['DEBUG_MODE']

    return local_constants

def get_args():
    """ Set up command line arguments """
    parser = argparse.ArgumentParser(description="Web Crawling script")
    parser.add_argument('-s', '--seeds', type=str, required=True, help="Path to seed file")
    parser.add_argument('-n', '--limit', type=int, required=True, help="Number of pages to crawl")
    parser.add_argument('-d', '--debug', action='store_true', help="Enable debug mode")

    # """ Simulating the python CLI arguments """

    if '__file__' not in globals():  # Detecta se está em um notebook
        params = ['-s', DEFAULT_PATH, '-n', DEFAULT_LIMIT, '-d']
        args = parser.parse_args(params)  # Ignora args ou simula
    else:
        args = parser.parse_args()   # Usa normalmente no terminal
    
    return args
