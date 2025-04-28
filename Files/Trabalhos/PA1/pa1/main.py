""" Importando as bibliotecas necessárias """

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
from warcio.warcwriter import WARCWriter # GPT is helping me with WARCing
from warcio.statusandheaders import StatusAndHeaders
from warcio.archiveiterator import ArchiveIterator # Needed for reading WARC files
import gzip # Needed for reading WARC files
from io import BytesIO # GPT is helping me with WARCing

# JV
import bs4 as bs # BeautifulSoup wrapper for parsing HTML and XML
import datetime # Getting unix timestamp
import json
import re # Splitting strings
import argparse # Parsing command line arguments
import sys
from collections import deque # Needed for the sitemap exploring
import time # Time functions
from concurrent.futures import ThreadPoolExecutor, as_completed # For multithreading
import os
from threading import Lock

from requests.exceptions import SSLError, ConnectTimeout, ReadTimeout, ConnectionError, RequestException



# Adicionar no início do script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

""" Simulating the python CLI arguments """

start_time = time.time()  # Start time for the entire script

partial_time = time.time()  # Start time for the partial checkpoint

def get_args():
    """ Set up command line arguments """
    parser = argparse.ArgumentParser(description="Web Crawling script")
    parser.add_argument('-s', '--seeds', type=str, required=True, help="Path to seed file")
    parser.add_argument('-n', '--limit', type=int, required=True, help="Number of pages to crawl")
    parser.add_argument('-d', '--debug', action='store_true', help="Enable debug mode")
    
    if '__file__' not in globals():  # Detecta se está em um notebook
        params = ['-s', '../Seeds/seeds-2024711370.txt', '-n', '100000', '-d']
        args = parser.parse_args(params)  # Ignora args ou simula
    else:
        args = parser.parse_args()   # Usa normalmente no terminal
    
    return args

ARGS = get_args()

# print(f"Arguments: {ARGS}")  # Debugging line to check the arguments passed to the script

""" Code constants: SEEDS_FILE, PAGES_LIMIT, DEBUG_MODE, MIN_DELAY, MAX_THREADS """

SEEDS_FILE = ARGS.seeds if ARGS.seeds else './Seeds/seeds-2024711370.txt'
PAGES_LIMIT = ARGS.limit if ARGS.limit else 2500
DEBUG_MODE = ARGS.debug if ARGS.debug else False
MIN_DELAY = 100 # Delay in milliseconds between requests
MAX_THREADS = 40 # Maximum number of threads to use for crawling
WARC_SIZE = 100 # Number of pages to write to a WARC file before creating a new one

""" print_json: Pretty print JSON data """

def print_json(data):
    """ Pretty prints JSON data. """
    def convert(obj):
        if isinstance(obj, set):
            return list(obj)
        if isinstance(obj, requests.structures.CaseInsensitiveDict):
            return dict(obj)
        raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')

    print(json.dumps(data, indent=4, default=convert))

""" default_requester: useful for removing try_except blocks from the main code """

def default_requester(url, timeout=5):
    """ Default function to make a GET request to a URL. """
    
    def cleaning_headers(headers):
        """ Clean headers not needed keys """
        new_headers = {
            'Content-Type': headers.get('Content-Type', ''),
            'Cache-Control': headers.get('Cache-Control', ''),
            'Content-Encoding': headers.get('Content-Encoding', ''),
            'Date': headers.get('Date', ''),
            'Strict-Transport-Security': headers.get('Strict-Transport-Security', ''),
            # 'X-Frame-Options': headers.get('X-Frame-Options', ''),
            # 'ETag': headers.get('ETag', ''),
            # 'Vary': headers.get('Vary', ''),
        }
        
        return new_headers
        
    
    def get_response_dict(response):
        """ Convert response to a dictionary. """
        response_dict = {
            'apparent_encoding': response.apparent_encoding,         # Returns the apparent encoding
            # 'close()': response.close,                               # Closes the connection to the server
            'content': response.content,                             # Returns the content of the response, in bytes
            'cookies': response.cookies,                             # Returns a CookieJar object with the cookies sent back from the server
            'elapsed': response.elapsed,                             # Returns a timedelta object with the time elapsed from sending the request to the arrival of the response
            'encoding': response.encoding,                           # Returns the encoding used to decode r.text
            'headers': response.headers,                             # Returns a dictionary of response headers
            'history': response.history,                             # Returns a list of response objects holding the history of request (url)
            'is_permanent_redirect': response.is_permanent_redirect, # Returns True if the response is the permanent redirected url, otherwise False
            'is_redirect': response.is_redirect,                     # Returns True if the response was redirected, otherwise False
            # 'iter_content()': response.iter_content,                 # Iterates over the response
            # 'iter_lines()': response.iter_lines,                     # Iterates over the lines of the response
            # 'json': response.json(),                                 # Returns a JSON object of the result (if the result was written in JSON format, if not it raises an error)
            'links': response.links,                                 # Returns the header links
            'next': response.next,                                   # Returns a PreparedRequest object for the next request in a redirection
            'ok': response.ok,                                       # Returns True if status_code is less than 400, otherwise False
            # 'raise_for_status()': response.raise_for_status,         # If an error occur, this method returns a HTTPError object
            'reason': response.reason,                               # Returns a text corresponding to the status code
            'request': response.request,                             # Returns the request object that requested this response
            'status_code': response.status_code,                     # Returns a number that indicates the status (200 is OK, 404 is Not Found)
            'text': response.text,                                   # Returns the content of the response, in unicode
            'url': response.url,                                     # Returns the URL of the response
            'version': response.raw.version,                             # Returns the version of the HTTP protocol used by the server
        }
        response_dict['headers'] = cleaning_headers(response_dict['headers'])
        return response_dict
    
    try:
        response = requests.get(url, timeout=timeout)
        # print(response.status_code)  # Print the status code of the response
        return get_response_dict(response)  # Call the function to get the response dictionary
    
    except SSLError as e:
        msg = f'-> {e}'
        print(f"[SSL ERROR]\t{url}")
        return None

    except ConnectTimeout as e:
        msg = f'-> {e}'
        print(f"[CONNECT TIMEOUT]\t{url}")
        return None

    except ReadTimeout as e:
        msg = f'-> {e}'
        print(f"[READ TIMEOUT]\t{url}")
        return None

    except ConnectionError as e:
        msg = f'-> {e}'
        print(f"[CONNECTION ERROR]\t{url}")
        return None

    except RequestException as e:
        msg = f'-> {e}'
        print(f"[REQUEST ERROR]\t{url}")
        return None

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


""" get_base_url: Get the base URL from a given URL """

def get_base_url(url):
    """ Get the base URL from a given URL. """
    
    parsed_url = requests.utils.urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return base_url

""" read_warc: Reads the WARC file and prints its contents. """

def read_warc_zipped_file(warc_path):
    """ Reads and prints the WARC file contents. """
    with open(warc_path, 'rb') as stream:
        if warc_path.endswith('.gz'):
            stream = gzip.GzipFile(fileobj=stream)

        for record in ArchiveIterator(stream):
            if record.rec_type == 'response':
                uri = record.rec_headers.get_header('WARC-Target-URI')
                payload = record.content_stream().read()
                print(f"URI: {uri}")
                print(f"Payload: {payload[:500]}...")  # Show first 500 bytes
                print("-" * 50)

# read_warc_zipped_file('output.warc.gz')

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

""" get_timestamp: Returns the current timestamp in seconds since 1970 """
    
def get_timestamp():
    """ Returns the current timestamp in seconds since 1970 """
    return int(datetime.datetime.now().timestamp())

def debug_time_elapsed():
    """ Returns the time elapsed since the start time """
    global start_time, partial_time
    end_time = time.time()
    
    from_last_checkpoint = end_time - partial_time
    from_start = end_time - start_time
    
    msg = f'TIMES: from start: {from_start:.2f} seconds\tfrom last save: {from_last_checkpoint:2f} seconds'
    print(msg)
    
    partial_time = end_time  # Update the checkpoint time

""" get_seeds: Getting seeds from file """

def get_seeds(path='./Seeds/seeds-2024711370.txt'):
    """ Reads all seeds from a file and returns them as a set. """
    seeds = set()
    with open(path, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):
                seeds.add(line)
    return seeds

""" get_robots_txt: processes the contents of the robots.txt file. """

def get_robots_txt(url):
    """ Returns the robots.txt file for a given URL. """
    def robots_scraping(robots_text):
        """ Processes the robots info """
        # Parse the robots.txt file and extract the rules
        rules = {
            'crawl-delay': MIN_DELAY,
            'user-agents': {},
            'sitemap': [],
            'misc': [],
        }
        lines = robots_text.splitlines()
        user_agent = None
        for line in lines:
            line = line.strip().lower()
            splitted_line = line.split(':', 1)

            key = splitted_line[0].strip()
            value = splitted_line[1].strip() if len(splitted_line) > 1 else ''
            if key == 'user-agent':
                user_agent = value
                if user_agent not in rules['user-agents']:
                    rules['user-agents'][user_agent] = { 'disallow': [], 'allow': []}
            
            elif key in ['disallow', 'allow'] and user_agent:
                rules['user-agents'][user_agent][key].append(value)
            elif key == 'crawl-delay' and user_agent:
                try:
                    rules[key] = int(value)
                except ValueError:
                    pass
            elif key == 'sitemap':
                rules[key].append(value)
            else:
                if len(line) > 0:
                    rules['misc'].append(line)
            
        return rules
        
    
    # Parse the URL to get the base domain
    parsed_url = requests.utils.urlparse(url)
    # print(type(parsed_url))
    # print(dict(parsed_url))
    robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
    
    try:
        response = requests.get(robots_url, timeout=5)
        if response.status_code == 200:
            return robots_scraping(response.text)
        else:
            print(f"Robots.txt not found for {url}. Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error fetching robots.txt for {url}: {e}")
    return None

""" get_sitemap: processes the contents of the sitemap.xml file. """

def get_sitemap(url, robots_info=None):
    def parse_sitemap(sitemap_url):
        """ Processes the sitemap XML and extracts URLs info """
        response = default_requester(sitemap_url)
        if response is None:
            return [set(), set()]
        sitemap_text = response.text
        soup = bs.BeautifulSoup(sitemap_text, 'xml')
        urls = list()
        xmls = list()
        
        # Extract URLs from the sitemap
        for url in soup.find_all('url'):
            loc = url.find('loc')
            urls.append(loc.text.strip()) if loc else None
        for sitemap in soup.find_all('sitemap'):
            loc = sitemap.find('loc')
            xmls.append(loc.text.strip()) if loc else None
        return [xmls, urls]
    
    def traverse_sitemaps(sitemap_info):
        sitemap_queue = deque(sitemap_info['sitemap_urls'])
        # index = 0
        while sitemap_queue:
            sitemap_url = sitemap_queue.popleft()
            [nested, pages] = parse_sitemap(sitemap_url)
            # [nested, pages] = benchmark_test(parse_sitemap, [sitemap_url])
            sitemap_queue.extend(nested)  # adiciona os sitemaps internos na fila
            sitemap_info['sitemap_urls'].extend(nested)  # adiciona os sitemaps internos na lista de sitemaps
            sitemap_info['found_urls'].extend(pages)
            
            # index += 1
            # msg = f'{index}/{len(sitemap_info["sitemap_urls"])}\t {sitemap_url}: pages: {len(sitemap_info["found_urls"])}'
            # print(msg)
            # print_json({'sitemaps': len(sitemap_info['sitemap_urls']), 'pages': len(sitemap_info['found_urls'])})

        return sitemap_info
    
    if len(robots_info['sitemap']) == 0:
        parsed_url = requests.utils.urlparse(url)
        sitemap_url = f"{parsed_url.scheme}://{parsed_url.netloc}/sitemap.xml"
        robots_info['sitemap'] = [sitemap_url]

    sitemap_info = {'found_urls': [], 'sitemap_urls': robots_info['sitemap'] }
    
    sitemap_info = traverse_sitemaps(sitemap_info)

    # print_json(sitemap_info)

    return sitemap_info

""" update_frontier: Adds a new URL to the frontier. """

def update_frontier(frontier, scraped_url):
    """ Updates the frontier with new links found in the parsed URL. """
    frontier.update(scraped_url['Outlinks'])
    return frontier

""" scrape_url: Parses a URL and returns its components. """

def scrape_url(url):
    """ Parses a URL and returns its components. """

    def first_words(text):
        """ Only get the 20 first words from the text (ignoring empty tokens) """
        # \W+ = qualquer sequência de caracteres que não sejam letras ou números
        words = re.split(r'\W+', text)
        # words = re.findall(r'\b\w[\w\'\-]*[!?.,]?\b', text) # Match palavras com pontuação leve grudada (.,!?, etc.)

        # remove vazios resultantes de split
        words = [word for word in words if word]
        joined_words = ' '.join(words[:20])
        return joined_words
    
    def get_new_links(soup):
        """ Returns all new links found in the parsed HTML. """
        links = set()
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith('http'):
                links.add(get_base_url(href))
        return links
        
    def clean_text(text):
        """ Cleans the text by removing excess whitespace and newlines. """
        cleaned_text = text.replace('\t', ' ') # Converts tabs to spaces
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text) # Remove excess whitespace
        cleaned_text = re.sub(r'\n+', '\n', cleaned_text) # Convert multiple newlines to a single newline
        return cleaned_text
    
    def get_useful_info(base_parsed_url, response):
        """ Returns useful information from the response. """
        soup = bs.BeautifulSoup(response['content'], 'html.parser')
        full_text = soup.get_text()
        cleaned_text = clean_text(full_text)
        
        base_parsed_url['Title'] = soup.title.string if soup.title else None
        base_parsed_url['Text'] = first_words(full_text)
        base_parsed_url['Timestamp'] = get_timestamp()
        
        base_parsed_url['Outlinks'] = get_new_links(soup)
        base_parsed_url['Full_Text'] = cleaned_text
        base_parsed_url['Headers'] = response['headers']
        # base_parsed_url['Raw'] = response['raw']
        base_parsed_url['Status_Code'] = response['status_code']
        base_parsed_url['Version'] = response['version']
        base_parsed_url['HTML'] = response['text']
        return base_parsed_url
    
    base_parsed_url = {
        'URL': url,
        'Title': '',
        'Text': '',
        'Timestamp': None,
        'Outlinks': set(),
        'Full_Text': '',
        'Headers': dict(),
        'Status_Code': None,
        'Version': None
    }
    response = default_requester(url)
    if response is None:
        return base_parsed_url
    
    mime = response['headers'].get('Content-Type', '').split(';')[0]
    status_code_200 = response['status_code'] == 200
    is_HTML = mime == 'text/html'
    # print_json(response)
    if status_code_200 and is_HTML:
        return get_useful_info(base_parsed_url, response)

    return base_parsed_url

""" store_warc: Stores the parsed URL in a WARC file. """

warc_lock = Lock()  # Lock for thread-safe writing to WARC files

def store_warc(parsed_url, index, warc_file_saving_method='ab', is_compressed=True):
    """ Stores the parsed URL in a WARC file. """

    def get_protocol_version(version):
        """ Returns the protocol version used in the response. """
        protocol  = f'unknown {version}'
        if version == 10:
            protocol = 'HTTP/1.0'
        elif version == 11:
            protocol = 'HTTP/1.1'
        elif version == 20:
            protocol = 'HTTP/2.0'
        return protocol

    output_path = f'WARCs/output_{index:03}.warc'
    if is_compressed:
        output_path += '.gz'

    headers = StatusAndHeaders(
        statusline=str(parsed_url['Status_Code']),
        headers={},
        # headers=parsed_url['Headers'].items(), # Mais completo, mas poluído.
        protocol=get_protocol_version(parsed_url['Version']),
    )

    # print_json(parsed_url['HTML'])
    # ab = Append and Binary mode.
    with open(output_path, warc_file_saving_method) as output:
        # gzip = True makes it automatically compressed.
        writer = WARCWriter(output, gzip=is_compressed)
        record = writer.create_warc_record(
            uri=parsed_url['URL'],
            record_type='response',
            payload=BytesIO(parsed_url['HTML'].encode('utf-8')),
            # payload=parsed_url['Raw'],
            http_headers=headers,
        )
        writer.write_record(record)


def store_warcs(scraping):
    """ Stores the parsed URLs in a WARC file. """
    with warc_lock:
        content = scraping['content']
        index = scraping['count'] // WARC_SIZE
        
        debug_time_elapsed()
        
        for parsed_url in content.values():
            store_warc(parsed_url, index, 'ab')

""" Scraping storage structure """

scraping = {
    'count': 0,
    'stored': 0,
    'content': dict(),
    'stored_urls': set(),  # Set of URLs already stored in WARC
    'frontier': get_seeds(SEEDS_FILE).copy(),  # Set of URLs to scrape
}

scraping['frontier'] = set([get_base_url(url) for url in scraping['frontier']])

""" Actual Scraping """

def debug_scrape_print(scraping, url):
    """ Prints the scraping state. """
    msg = f'({scraping["count"]:04}/{len(scraping["frontier"]):04})\t'
    msg += url
    # msg += f' => {PAGES_LIMIT}'
    # first_3_plus_last_3 = list(scraping['frontier'])[:2] + list(scraping['frontier'])[-2:]
    # msg += f'\nFrontier: {first_3_plus_last_3}'
    # msg_debug_repeat = f'({scraping["count"]}): 
    print(msg)
    # print_json(scraping)
    # if scraping['count'] % 100 == 0:  # Print status every 100 iterations

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
    scraping['content'][url] = parsed_url
    scraping['frontier'] = update_frontier(scraping['frontier'], parsed_url)
    scraping['count'] += 1  # Increment the count of pages scraped
    
    if scraping['count'] % WARC_SIZE == 0:
        # Store the parsed URL in a WARC file and clean up the content
        print(f">>> Storing WARC file for {scraping['count']} pages... <<<")
        store_warcs(scraping)
        scraping['content'] = dict()
        scraping['stored'] += 1

    debug_scrape_print(scraping, url)

def parallel_scrape(function, scraping, max_workers=MAX_THREADS):
    """ Parallel scraping function using ThreadPoolExecutor. """

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = set()

        # Primeiro, preenche até o máximo inicial
        while scraping['frontier'] and len(futures) < max_workers:
            futures.add(executor.submit(function, scraping))

        while futures:
            # Espera qualquer uma terminar
            for future in as_completed(futures):
                futures.remove(future)
                try:
                    future.result()
                except Exception as e:
                    print(f"Erro durante scraping: {e}")

                # Quando uma terminar, tenta lançar outra
                if scraping['frontier'] and scraping['count'] < PAGES_LIMIT:
                    futures.add(executor.submit(function, scraping))
                break  # Importante: sair do for depois de pegar UM terminado

parallel_scrape(scrape_once, scraping, 50)

print(f"Total execution time: {time.time() - start_time:.2f} seconds")