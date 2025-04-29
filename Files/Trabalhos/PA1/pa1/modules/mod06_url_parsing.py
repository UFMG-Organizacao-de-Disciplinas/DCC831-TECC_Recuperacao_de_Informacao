""" Parse URL module """

# Importing my modules

from modules.mod04_utils import get_timestamp, default_requester, get_base_url # HTTP request handling functions

# Importing my needed libraries

import re # Splitting strings
import bs4 as bs # BeautifulSoup wrapper for parsing HTML and XML

# Scraping functions

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
        'Version': None,
        'HTML': '',
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
