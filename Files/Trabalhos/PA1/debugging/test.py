""" Testando argparse para o crawler """

import argparse

parser = argparse.ArgumentParser(description='Simple Web Crawler')

parser.add_argument('-s', '--seeds', required=True, help='Path to seed file')
parser.add_argument('-n', '--limit', type=int, required=True,
                    help='Number of pages to crawl')
parser.add_argument('-d', '--debug', action='store_true',
                    help='Run in debug mode')

args = parser.parse_args()

print(args)

print("Sua semente é: ", args.seeds)

print("Seu limite é: ", args.limit)

print("Modo debug: ", args.debug)
