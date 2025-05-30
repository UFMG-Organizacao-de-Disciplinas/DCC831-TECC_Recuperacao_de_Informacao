""" Indexer


## Indexer

Your implementation must include an `indexer.py` file, which will be executed in the same virtual environment described above, as follows:

```bash
python3 indexer.py -m <MEMORY> -c <CORPUS> -i <INDEX>
```

with the following arguments:

- `-m <MEMORY>`: the memory available to the indexer in megabytes.
- `-c <CORPUS>`: the path to the corpus file to be indexed.
- `-i <INDEX>`: the path to the directory where indexes should be written.

At the end of the execution, your indexer.py implementation must print a JSON document to standard output [$^1$][Note_1] with the following statistics:

- `Index Size`: the index size in megabytes;
- `Elapsed Time`: the time elapsed (in seconds) to produce the index;
- `Number of Lists`: the number of inverted lists in the index;
- `Average List Size`: the average number of postings per inverted list.

The following example illustrates the required output format:

```json
{
  "Index Size": 2354,
  "Elapsed Time": 45235,
  "Number of Lists": 437,
  "Average List Size": 23.4
}
```

### Document Corpus

The corpus to be indexed comprises structured representations (with id, title, descriptive text, and keywords) for a total of 4,641,784 named entities present in Wikipedia. These structured representations are encoded as `JSON` documents in a single `JSONL` file available for download.[$^2$][Note_2] To speed up development, you are encouraged to use a smaller portion of the corpus to test your implementation before you try to index the complete version.

### Indexing Policies

For each document in the corpus (the `-c` argument above), your implementation must parse, tokenize, and index it. Your implementation must operate within the designated memory budget (the `-m` argument) during its entire execution. [$^3$][Note_3] [$^4$][Note_4] This emulates the most typical scenario where the target corpus far exceeds the amount of physical memory available to the indexer. At the end of the execution, a final representation of all produced index structures (inverted index, document index, term lexicon) must be stored as three separate files, one for each structure, at the designated directory (the `-i` argument).

In addition to this workflow, your implementation **must abide by the following policies**, which will determine your final grade in this assignment:

1. _Pre-processing Policy_: To reduce the index size, your implementation **must perform stopword removal and stemming**. Additional preprocessing techniques can be implemented at your discretion.

2. _Memory Management Policy_: To ensure robustness, your implementation **must execute under limited memory availability**. To this end, it must be able to produce partial indexes in memory (respecting the imposed memory budget) and merge them on disk. [$^5$][Note_5]

3. _Parallelization Policy_: To ensure maximum efficiency, you **must parallelize the indexing process across multiple threads**. You may experiment to find an optimal number of threads to minimize indexing time rate while minimizing the incurred parallelization overhead.

4. _Compression Policy (extra)_: Optionally, **you may choose to implement a compression scheme for index entries** (e.g. gamma for docids, unary for term frequency) for maximum storage efficiency.

[Note_1]: https://en.wikipedia.org/wiki/Standard_streams#Standard_output_(stdout)
[Note_2]: https://www.kaggle.com/datasets/rodrygo/entities
[Note_3]: <> "The memory limit will be strictly enforced during grading. If your program exceeds it, it may be automatically terminated with an out-of-memory (OOM) error. To prevent this, use `psutil.Process(os.getpid()).memory_info().rss` to monitor your current memory usage (in bytes), and offload partial indexes to disk before allocating more memory as needed."
[Note_4]: <> "Note that the memory budget refers to the total memory available to your implementation, not only to the memory needed to store the actual index structures. As a reference lower bound, assume your implementation will be tested with `-m 1024`."
[Note_5]: https://en.wikipedia.org/wiki/External_sorting#External_merge_sort

"""

import time  # Time tracking
import json  # Pretty prints JSON
import argparse  # Argument parsing
import os  # File operations

START_TIME = time.time()
INDEX_PATH = "index.json"  # Default index path


def get_indexer_args():
    """ Return a dictionary of the needed arguments, those being:
        -m <MEMORY> : Memory in MB
        -c <CORPUS> : Corpus path
        -i <INDEX>  : Index path
    """

    parser = argparse.ArgumentParser(description="Indexer arguments")
    parser.add_argument("-m", "--memory", type=int,
                        required=True, help="Memory in MB")
    parser.add_argument("-c", "--corpus", type=str,
                        required=True, help="Corpus path")
    parser.add_argument("-i", "--index", type=str,
                        required=True, help="Index path")
    args = parser.parse_args()
    args_dict = vars(args)
    return args_dict


def compute_statistics(local_start_time=0, index_path="index.json"):
    """ Compute statistics for the indexer """

    def get_index_size(index_path):
        """ Get the size of the index in MB """
        if not os.path.exists(index_path):
            return None

        size = os.path.getsize(index_path)
        size_in_mb = size / (1024 * 1024)

        return size_in_mb

    def get_number_of_lists(index_path):
        """ Get the number of inverted lists in the index """
        if not os.path.exists(index_path):
            return None

        with open(index_path, 'r', encoding='utf8') as f:
            index_data = json.load(f)

        # Assuming the index is a dictionary where keys are terms
        number_of_lists = len(index_data)
        return number_of_lists

    def get_average_number_of_postings(index_path):
        """ Get the average number of postings per inverted list """
        if not os.path.exists(index_path):
            return None

        with open(index_path, 'r', encoding='utf8') as f:
            index_data = json.load(f)

        total_postings = 0
        number_of_lists = len(index_data)

        for _, postings in index_data.items():
            total_postings += len(postings)

        if number_of_lists == 0:
            return 0

        # Calculate average postings per list
        average_postings = total_postings / number_of_lists

        return average_postings

    statistics = {
        "Index Size": get_index_size(index_path),  # in MB
        "Elapsed Time": time.time() - local_start_time,  # in seconds
        # number of inverted lists
        "Number of Lists": get_number_of_lists(index_path),
        # average number of postings per inverted list
        "Average List Size": get_average_number_of_postings(index_path)
    }

    return statistics


def print_json(data):
    """ Print the data in JSON format """
    print(json.dumps(data, indent=4))


def main():
    """ indexer base """
    get_indexer_args()
    statistics = compute_statistics(START_TIME, INDEX_PATH)
    print_json(statistics)


main()
