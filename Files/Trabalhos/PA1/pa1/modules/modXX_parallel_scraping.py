
def parallel_scrape(function, scraping, max_workers=MAX_THREADS):
    """ Parallel scraping function using ThreadPoolExecutor. """

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = set()

        # Primeiro, preenche até o máximo inicial
        while scraping['frontier'] and len(futures) < max_workers:
            futures.add(executor.submit(function, scraping))

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
            while scraping['frontier'] and len(futures) < max_workers and scraping['count'] < PAGES_LIMIT:
                futures.add(executor.submit(function, scraping))
