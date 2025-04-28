""" Robots and Sitemaps Module """

# Importing my modules

from modules.mod04_utils import default_requester, contants # Needed for the default requester

# Importing my needed libraries

import bs4 as bs # BeautifulSoup wrapper for parsing HTML and XML
from collections import deque # Needed for the sitemap exploring
import requests # Needed for HTTP requests

# Parsing robots.txt and sitemaps

def get_robots_txt(url):
    """ Returns the robots.txt file for a given URL. """
    def robots_scraping(robots_text):
        """ Processes the robots info """
        # Parse the robots.txt file and extract the rules
        rules = {
            'crawl-delay': contants()['MIN_DELAY'],
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
