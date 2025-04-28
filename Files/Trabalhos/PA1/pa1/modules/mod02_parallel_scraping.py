""" Parallel scraping module """

# Importing my modules

from modules.mod04_utils import get_seeds

# Importing my needed libraries

from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED # For multithreading

# Parallel scraping function

def parallel_scrape(scrape_func, CONSTANTS):
    """ Parallel scraping function using ThreadPoolExecutor. """
    # Scraping storage structure
    scraping = {
        'count': 0,
        'stored': 0,
        'content': dict(),
        'stored_urls': set(),  # Set of URLs already stored in WARC
        'frontier': get_seeds(CONSTANTS['SEEDS_PATH']),  # Set of URLs to scrape
    }

    with ThreadPoolExecutor(max_workers=CONSTANTS['MAX_THREADS']) as executor:
        futures = set()

        # Primeiro, preenche até o máximo inicial
        while scraping['frontier'] and len(futures) < CONSTANTS['MAX_THREADS']:
            futures.add(executor.submit(scrape_func, scraping))

        while futures:
            # Espera qualquer uma terminar
            done, futures = wait(futures, return_when=FIRST_COMPLETED)

            for future in done:
                # print(f'[THREADS: {len(futures)}||{threading.active_count()}]')
                try:
                    future.result()
                except Exception as e:
                    print(f"Erro durante scraping: {e}")

            # Depois que uma ou mais futures terminam, tentar preencher de novo até o máximo
            while scraping['frontier'] and len(futures) < CONSTANTS['MAX_THREADS'] and scraping['count'] < CONSTANTS['CORPUS_SIZE']:
                futures.add(executor.submit(scrape_func, scraping))
