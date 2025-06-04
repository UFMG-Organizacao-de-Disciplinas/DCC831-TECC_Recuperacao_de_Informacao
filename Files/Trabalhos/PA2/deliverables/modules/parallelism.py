""" Module for dealing with parallelism in indexing operations. """

import threading
import os
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

from auxiliar import get_memory_usage


# === Locks for Thread Safety ===

LOCKS = {
    'inverted_index.json': threading.Lock(),
    'document_index.json': threading.Lock(),
    'term_lexicon.json': threading.Lock()
}


def get_lock(file_path):
    """ Gets the lock for the given file path """
    file_name = os.path.basename(file_path)
    specific_lock = LOCKS.get(file_name, threading.Lock())
    # This second lock ensures that if the file is not in the predefined locks,
    # a new lock is created for it,
    return specific_lock

# === Safe Threaded File Operations ===


def safe_load_json(file_path):
    """ Loads JSON with appropriate locking mechanism """
    lock = get_lock(file_path)
    with lock:
        if not os.path.exists(file_path):
            return {}
        with open(file_path, 'r', encoding='utf8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print(f"Invalid path: {file_path}")
                return {}


def safe_save_json(file_path, data):
    """ Saves JSON with appropriate locking mechanism"""
    lock = get_lock(file_path)
    with lock:
        with open(file_path, 'w', encoding='utf8') as f:
            json.dump(data, f, ensure_ascii=False)

# === Indexer Parallelism ===


def parallel_index(cmd_args, doc_processing_function, limit, max_threads=8):
    """Gerencia o paralelismo no processamento do corpus"""
    memory_limit = cmd_args['memory']
    index_path = cmd_args['index']

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = []
        with open(cmd_args['corpus'], 'r', encoding='utf8') as f:
            for idx, line in enumerate(f):
                current_mem = get_memory_usage(index_path)
                if current_mem > memory_limit:
                    msg = f"[{idx:05d}] ❌ Memória ({current_mem:.2f} MB) excedeu o limite"
                    msg += f"({memory_limit} MB). Parando."
                    print(msg)
                    break

                if limit and idx >= limit:
                    print("=== Threads criadas ===")
                    break

                # Agenda processamento de documento
                futures.append(executor.submit(
                    doc_processing_function, line, index_path, idx))

        # Acompanha a execução das threads
        for i, future in enumerate(as_completed(futures), 1):
            try:
                future.result()
                # print(f"[{i:05d}] ✅ Documento processado.")
            except Exception as e:
                print(f"[{i:05d}] ❌ Erro: {e}")


def new_parallel_index(cmd_args, doc_processing_function, limit, max_threads=8):
    """ This new version of parallel_index is designed to handle large corpora in a more
        reasonable way. It divides the corpus into chunks and processes them in parallel,
        while monitoring memory usage.
        It will:
            - Divide the corpus into chunks based on the number of threads.
            - Process each chunk in a separate thread.
            - Monitor memory usage and restart threads if they exceed the limit.
            - A new thread will be created following the last processed document in the
              previous thread.
    """
