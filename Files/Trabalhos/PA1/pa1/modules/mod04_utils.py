""" Utility functions for the project. """

# Importing my modules

from modules.mod00_debugging import print_json

# Importing my needed libraries

import requests
from requests.utils import urlparse
from requests.exceptions import SSLError, ConnectTimeout, ReadTimeout, ConnectionError, RequestException
import os
from time import time # Getting unix timestamp

# Utility functions

def set_working_directory(file_path):
    # Adicionar no início do script
    print(file_path)
    os.chdir(os.path.dirname(os.path.abspath(file_path)))

def get_base_url(url):
    """ Get the base URL from a given URL, only with the scheme and netloc. """
    
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return base_url

def get_timestamp():
    """ Returns the current timestamp in seconds since 1970 """
    return int(time())

def get_seeds(path):
    """ Reads all seeds from a file and returns them as a set. """
    seeds = set()
    with open(path, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):
                seeds.add(get_base_url(line))
    return seeds

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
    
    except SSLError:
        #  as e msg = f'-> {e}'
        print(f"[SSL ERROR]\t{url}")
        return None

    except ConnectTimeout:
        #  as e msg = f'-> {e}'
        print(f"[CONNECT TIMEOUT]\t{url}")
        return None

    except ReadTimeout:
        #  as e msg = f'-> {e}'
        print(f"[READ TIMEOUT]\t{url}")
        return None

    except ConnectionError:
        #  as e msg = f'-> {e}'
        print(f"[CONNECTION ERROR]\t{url}")
        return None

    except RequestException:
        #  as e msg = f'-> {e}'
        print(f"[REQUEST ERROR]\t{url}")
        return None

def debug_print(parsed_url):
    """ Prints the parsed URL in a readable format that is defined in the assignment. """
    debug_info = {
        'URL': parsed_url['URL'],
        'Title': parsed_url['Title'],
        'Text': parsed_url['Text'],
        'Timestamp': parsed_url['Timestamp'],
    }
    print_json(debug_info)