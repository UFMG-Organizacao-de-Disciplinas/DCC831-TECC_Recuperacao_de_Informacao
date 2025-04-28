import argparse # Parsing command line arguments

""" Simulating the python CLI arguments """

def get_args(constants):
    """ Set up command line arguments """
    parser = argparse.ArgumentParser(description="Web Crawling script")
    parser.add_argument('-s', '--seeds', type=str, required=True, help="Path to seed file")
    parser.add_argument('-n', '--limit', type=int, required=True, help="Number of pages to crawl")
    parser.add_argument('-d', '--debug', action='store_true', help="Enable debug mode")
    
    if '__file__' not in globals():  # Detecta se está em um notebook
        params = ['-s', constants['SEEDS_PATH'], '-n', constants['CORPUS_SIZE'], '-d']
        args = parser.parse_args(params)  # Ignora args ou simula
    else:
        args = parser.parse_args()   # Usa normalmente no terminal
    
    return args

