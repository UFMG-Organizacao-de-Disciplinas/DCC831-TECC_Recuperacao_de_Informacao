""" WEB Scraper for Programming Assignment 1 """

# Importing my modules

from modules.mod01_constants import constants # Constants for the scraper
from modules.mod02_parallel_scraping import parallel_scrape # Parallel scraping functions
from modules.mod03_scraping import scrape_once # Scraping function for a single URL
from modules.mod04_utils import set_working_directory # Utility functions

# Importing my needed libraries

import time # Time functions

# Importing suggested libraries

# import beautifulsoup4 as bs
# import certifi                          # Root certificates for validating SSL/TLS (used by requests)
# import charset_normalizer               # Used for detecting and normalizing text encodings (dependency of requests)
# import idna                             # Internationalized domain name support (dependency of requests)
# from protego import Protego             # Parses and enforces robots.txt rules
# import requests                         # HTTP library for making requests to web resources
# import six                              # Compatibility layer for writing Python 2/3 code (used by many older libs)
# import soupsieve                        # CSS selector engine for BeautifulSoup
# import typing_extensions                # Adds backported or experimental typing features for older Python versions
# from url_normalize import url_normalize # Normalizes URLs into a consistent format
# import urllib3                          # Low-level HTTP library used by requests
# import warcio                           # Library for reading and writing WARC (Web ARChive) files
# from warcio.capture_http import capture_http # Capture HTTP requests and responses for archiving

# Global variables

start_time = time.time()  # Start time for the entire script

# Main function

set_working_directory(__file__) # Set the working directory to the script's location
CONSTANTS = constants() # Load constants from the configuration file
parallel_scrape(scrape_once, CONSTANTS) # Actual Scraping

print(f"Total execution time: {time.time() - start_time:.2f} seconds")