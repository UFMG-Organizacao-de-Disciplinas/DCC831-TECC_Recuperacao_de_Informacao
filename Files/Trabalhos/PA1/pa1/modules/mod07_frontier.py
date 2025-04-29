""" update_frontier: Adds a new URL to the frontier. """

# Update frontier function

def update_frontier(scraping, scraped_url):
    """ Updates the frontier with new links found in the parsed URL thar weren't scraped neither stored """
    frontier = scraping['frontier']
    stored = scraping['stored_urls']
    # parsed_urls = set(scraping['content'].keys())
    outlinks = set(scraped_url['Outlinks'])
    # Adds new links to the frontier
    
    # Converte para conjunto para aproveitar operações eficientes
    # new_links = outlinks - stored - parsed_urls
    new_links = outlinks - stored
    
    # Adiciona os novos links à frontier
    frontier.update(new_links)
    
    return frontier