""" Scraping module for web crawling and data extraction. """

# Importing my modules

# from modules.mod00_debugging import debug_scrape_print, print_json
from modules.mod01_constants import constants
from modules.mod04_utils import debug_print
from modules.mod06_url_parsing import scrape_url
from modules.mod07_frontier import update_frontier
# from modules.mod08_WARC_handling import store_warcs, parallel_store_warcs
# from modules.mod08_WARC_handling import parallel_store_warcs
from modules.mod08_WARC_handling import warc_as_you_go

# Global variables

CONSTANTS = constants()
MAX_THREADS = CONSTANTS['MAX_THREADS'] # Maximum number of threads to use for crawling
PAGES_LIMIT = CONSTANTS['CORPUS_SIZE'] # Number of pages to write to a WARC file before creating a new one
WARC_SIZE = CONSTANTS['WARC_SIZE'] # Number of pages to write to a WARC file before creating a new one

# Scraping function

def scrape_once(scraping):
    """ Scrapes a single URL and updates the scraping state. """

    def is_scrapable(scraping):
        """ Checks if there are URLs to scrape and if the limit has not been reached. """
        if scraping['count'] >= PAGES_LIMIT:  # Check if the limit has been reached
            print(f"Scraping limit reached: {PAGES_LIMIT} pages.")
            return False
        if not scraping['frontier']:  # Check if the frontier is empty
            print("No more URLs to scrape.")
            return False
        return True

    def was_scraped(url, scraped_content):
        """ Checks if the URL has already been scraped. """
        if url in scraped_content:
            print(f"[SCRAPED]\t{url}")
            return True
        return False

    if not is_scrapable(scraping):
        return None

    url = scraping['frontier'].pop()
    
    if was_scraped(url, scraping['content']):
        return None

    parsed_url = scrape_url(url)
    # scraping['content'][url] = parsed_url
    scraping['frontier'] = update_frontier(scraping, parsed_url)
    scraping['count'] += 1  # Increment the count of pages scraped

    warc_as_you_go(scraping, parsed_url, is_compressed=True)

    # print_json(scraping)
    
    # if scraping['count'] % WARC_SIZE == 0:
        # Store the parsed URL in a WARC file and clean up the content
        # parallel_store_warcs(scraping)
        # store_warcs(scraping)

    if CONSTANTS['DEBUG_MODE']:
        # debug_scrape_print(scraping, url)
        debug_print(parsed_url)


