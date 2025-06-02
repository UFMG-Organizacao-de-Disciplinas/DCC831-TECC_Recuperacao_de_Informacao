""" Auxiliary functions for the project.
    - Argsparsing: Functions to parse command line arguments.
    - Memory Management: Functions to check memory usage.
    - JSON Printing: Functions to print JSON data in a readable format.
"""

import argparse
import json
import os
from threading import active_count  # Count the number of active threads
import psutil


def get_memory_usage(index_path, debug=False, idx=0):
    """ Get the current memory usage of the process in MB """
    def convert_bytes_to_mb(bytes_value):
        """ Convert bytes to megabytes """
        return bytes_value / (1024 * 1024)

    process_cost = psutil.Process(os.getpid()).memory_info().rss

    files_size = {
        'inverted_index.json': 0,
        'document_index.json': 0,
        'term_lexicon.json': 0
    }

    total_files_size = 0.0
    for file_name in files_size:
        file_path = os.path.join(index_path, file_name)

        if os.path.isfile(file_path):
            file_size = os.path.getsize(file_path)
            files_size[file_name] = file_size
            total_files_size += file_size

    # print_json(files_size)

    total_size = convert_bytes_to_mb(process_cost + total_files_size)
    msg = "Debug |Thd|Idx|Tot|Pcss|DI|II|TL|: "
    msg += f"|{active_count()-1:02d}"
    msg += f"|{idx:02d}"
    msg += f"|{total_size:.2f}"
    msg += f"|{convert_bytes_to_mb(process_cost):.2f}"
    msg += f"|{convert_bytes_to_mb(files_size['document_index.json']):.2f}"
    msg += f"|{convert_bytes_to_mb(files_size['inverted_index.json']):.2f}"
    msg += f"|{convert_bytes_to_mb(files_size['term_lexicon.json']):.2f}"
    msg += "| MB"
    if debug:
        print(msg)
    return total_size


def get_indexer_args():
    """ Return a dictionary of the needed arguments, those being:
        -m <MEMORY> : Memory in MB
        -c <CORPUS> : Corpus path
        -i <INDEX>  : Index path
    """

    parser = argparse.ArgumentParser(description="Indexer arguments")
    parser.add_argument("-m", "--memory", help="Memory in MB",
                        required=True, type=int)
    parser.add_argument("-c", "--corpus", help="Corpus path",
                        required=True, type=str)
    parser.add_argument("-i", "--index", help="Index path",
                        required=True, type=str)
    args = parser.parse_args()
    args_dict = vars(args)

    return args_dict


def print_json(data):
    """ Print the data in JSON format """
    print(json.dumps(data, indent=4))
def get_processor_args():
    """
    - `-i <INDEX>`: the path to an index file.
    - `-q <QUERIES>`: the path to a file with the list of queries to process.
    - `-r <RANKER>`: a string informing the ranking function (either "TFIDF" or "BM25") to be used
    to score documents for each query.
    """
    parser = argparse.ArgumentParser(description="Processor arguments")
    parser.add_argument("-i", "--index", required=True,
                        help="path to an index file")
    parser.add_argument("-q", "--queries", required=True,
                        help="path to queries")
    parser.add_argument("-r", "--ranker", required=True, help="ranking function to use",
                        choices=["TFIDF", "BM25"])
    args = parser.parse_args()
    args_dict = vars(args)

    return args_dict
