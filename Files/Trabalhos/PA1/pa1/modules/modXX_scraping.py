
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
    scraping['frontier'] = update_frontier(scraping, parsed_url)
    scraping['count'] += 1  # Increment the count of pages scraped
    
    if scraping['count'] % WARC_SIZE == 0:
        # Store the parsed URL in a WARC file and clean up the content
        print(f">>> Storing WARC file for {scraping['count']} pages... <<<")
        store_warcs(scraping, WARC_SIZE, debug_time_elapsed)
        scraping['content'] = dict()
        scraping['stored'] += 1

    debug_scrape_print(scraping, url)


