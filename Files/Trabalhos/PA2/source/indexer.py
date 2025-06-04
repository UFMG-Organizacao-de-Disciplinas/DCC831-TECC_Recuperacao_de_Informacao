""" ## Indexer

Your implementation must include an `indexer.py` file, which will be executed in the same virtual
environment described above, as follows:

```bash
python3 indexer.py -m <MEMORY> -c <CORPUS> -i <INDEX>
```

with the following arguments:

- `-m <MEMORY>`: the memory available to the indexer in megabytes.
- `-c <CORPUS>`: the path to the corpus file to be indexed.
- `-i <INDEX>`: the path to the directory where indexes should be written.

At the end of the execution, your indexer.py implementation must print a JSON document to standard
output [$^1$][Note_1] with the following statistics:

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

The corpus to be indexed comprises structured representations (with id, title, descriptive text,
and keywords) for a total of 4,641,784 named entities present in Wikipedia. These structured
representations are encoded as `JSON` documents in a single `JSONL` file available for
download.[$^2$][Note_2] To speed up development, you are encouraged to use a smaller portion of the
corpus to test your implementation before you try to index the complete version.

### Indexing Policies

For each document in the corpus (the `-c` argument above), your implementation must parse, tokenize,
and index it. Your implementation must operate within the designated memory budget (the `-m`
argument) during its entire execution. [$^3$][Note_3] [$^4$][Note_4] This emulates the most typical
scenario where the target corpus far exceeds the amount of physical memory available to the indexer.
At the end of the execution, a final representation of all produced index structures (inverted
index, document index, term lexicon) must be stored as three separate files, one for each structure,
at the designated directory (the `-i` argument).

In addition to this workflow, your implementation **must abide by the following policies**, which
will determine your final grade in this assignment:

1. _Pre-processing Policy_: To reduce the index size, your implementation **must perform stopword
removal and stemming**. Additional preprocessing techniques can be implemented at your discretion.

2. _Memory Management Policy_: To ensure robustness, your implementation **must execute under
limited memory availability**. To this end, it must be able to produce partial indexes in memory
(respecting the imposed memory budget) and merge them on disk. [$^5$][Note_5]

3. _Parallelization Policy_: To ensure maximum efficiency, you **must parallelize the indexing
process across multiple threads**. You may experiment to find an optimal number of threads to
minimize indexing time rate while minimizing the incurred parallelization overhead.

4. _Compression Policy (extra)_: Optionally, **you may choose to implement a compression scheme
for index entries** (e.g. gamma for docids, unary for term frequency) for maximum storage
efficiency.

#Standard_output_(stdout)
[Note_1]: https://en.wikipedia.org/wiki/Standard_streams

[Note_2]: https://www.kaggle.com/datasets/rodrygo/entities

[Note_3]: <> "The memory limit will be strictly enforced during grading. If your program exceeds it,
it may be automatically terminated with an out-of-memory (OOM) error. To prevent this, use
`psutil.Process(os.getpid()).memory_info().rss` to monitor your current memory usage (in bytes), and
offload partial indexes to disk before allocating more memory as needed."

[Note_4]: <> "Note that the memory budget refers to the total memory available to your
implementation, not only to the memory needed to store the actual index structures. As a reference
lower bound, assume your implementation will be tested with `-m 1024`."

[Note_5]: https://en.wikipedia.org/wiki/External_sorting#External_merge_sort

"""

import time  # Time tracking
import json  # Pretty prints JSON
import os  # File operations
import numpy as np  # Counting repeated terms

# My modules

from modules.auxiliar import get_indexer_args, print_json, get_memory_usage
# paralelism module for thread-safe file operations
from modules.parallelism import safe_load_json, safe_save_json, parallel_index
from modules.preprocessing import preprocess_text

FORCE_CREATE = True  # Force creation of index files even if they already exist
DEBUGGING = False  # Debugging mode, prints additional information

# convert all terms to its id
# limit amount of threads created to be used later in parallel_index


def compute_statistics(local_start_time=0.0, index_path="index.json"):
    """ Compute statistics for the indexer """

    def get_index_size(index_path):
        """ Get the size of the index in MB """
        if not os.path.exists(index_path):
            return None

        size = os.path.getsize(index_path)
        size_in_mb = size / (1024 * 1024)

        return size_in_mb

    def get_number_and_average(index_path):
        """ Get the number of inverted lists in the index
            and the average number of postings per inverted list
        """

        postings_info = {'Number of Lists': 0, 'Average List Size': 0.0}

        if not os.path.exists(index_path):
            return postings_info

        try:
            with open(index_path, 'r', encoding='utf8') as f:
                index_data = json.load(f)

            num_lists = len(index_data)
            if num_lists == 0:
                return postings_info

            total_postings = sum(len(postings)
                                 for postings in index_data.values())

            postings_info['Number of Lists'] = num_lists
            postings_info['Average List Size'] = total_postings / num_lists

        except (IOError, json.JSONDecodeError) as e:
            print(f"Erro ao processar arquivo: {e}")

        return postings_info

    inverted_index_path = os.path.join(index_path, 'inverted_index.json')
    postings_info = get_number_and_average(inverted_index_path)

    statistics = {
        # in MB
        "Index Size": get_index_size(inverted_index_path),
        "Elapsed Time": time.time() - local_start_time,  # in seconds
        # number of inverted lists
        "Number of Lists": postings_info['Number of Lists'],
        # average number of postings per inverted list
        "Average List Size": postings_info['Average List Size']
    }

    statistics['Index Size'] = int(statistics['Index Size'])
    statistics['Elapsed Time'] = int(statistics['Elapsed Time'])
    statistics['Average List Size'] = round(statistics['Average List Size'], 1)

    return statistics


def generate_structures(index_path):
    """ Generate the index structures (inverted index, document index, term lexicon) """

    def create_file(index_path, file_path):
        """ Create a file if it does not exist """
        index_structure_file_path = os.path.join(index_path, file_path)
        if not os.path.exists(file_path) or FORCE_CREATE:
            with open(index_structure_file_path, 'w', encoding='utf8') as f:
                json.dump({}, f, indent=4)

    create_file(index_path, 'inverted_index.json')
    create_file(index_path, 'document_index.json')
    create_file(index_path, 'term_lexicon.json')


def pre_processing(doc):
    """ Pre-process the document (stopword removal and stemming) """
    doc['text'] = preprocess_text(doc['text'])
    doc['title'] = preprocess_text(doc['title'])
    doc['keywords'] = [preprocess_text(keyword) for keyword in doc['keywords']]


def append_to_structures(doc, index_path):
    """ Append the processed document to the index structures """

    def append_to_term_lexicon(doc, output_dir):
        """ Add term lexicon entries for the document
            - This is meant to create a mapping of terms to IDs
            - Also, it updates the terms histogram
            Code:
            - loads the existing term lexicon or creates a new one
            - updates the terms to id mappings
            - updates the terms histogram
        """

        term_hist = 'terms_histogram'

        lexicon_path = os.path.join(output_dir, 'term_lexicon.json')
        term_lexicon = safe_load_json(lexicon_path)

        term_lexicon['term2id'] = term_lexicon.get('term2id', {})
        term_lexicon[term_hist] = term_lexicon.get(term_hist, {})

        for term, count in doc[term_hist].items():
            if term not in term_lexicon['term2id']:
                # Assign a new ID to the term
                term_id = str(len(term_lexicon['term2id']))
                term_lexicon['term2id'][term] = term_id
            else:
                term_id = str(term_lexicon['term2id'][term])
            # update terms histogram
            # int_term_id = int(term_id)
            # str_term_id = str(term_id)
            # print(str_term_id, int_term_id, term_lexicon)

            # If the term ID is not in the histogram, initialize it
            if term_id not in term_lexicon[term_hist]:
                term_lexicon[term_hist][term_id] = 0
            # term_lexicon[term_hist][term_id] = term_lexicon[term_hist].get(
            #     term_id, 0)
            term_lexicon[term_hist][term_id] += int(count)

            if term_id in [2, 3, 4, 5] and DEBUGGING:
                print(20*' = ')
                print(f"Term: {term}, ID: {term_id}, Count: {count}")
                print(term_lexicon[term_hist].get(term_id, 0))
                print(20*' = ')

        # Save the updated term lexicon
        safe_save_json(lexicon_path, term_lexicon)

    def append_to_inverted_index(doc, output_dir):
        """ Add inverted index entries for the document
            Only the text field is indexed, title and keywords are not indexed
            Also, only the existance of the term is indexed, not its frequency
        """
        inverted_index_path = os.path.join(output_dir, 'inverted_index.json')
        # print(inverted_index_path)
        # Load existing inverted index or create a new one

        inverted_index = safe_load_json(inverted_index_path)

        for term, count in doc['terms_histogram'].items():
            # count = term['terms_histogram'][term]
            if term not in inverted_index:
                inverted_index[term] = []
            posting = (doc['id'], count)
            inverted_index[term].append(posting)

        # Save the updated inverted index
        safe_save_json(inverted_index_path, inverted_index)

    def append_to_document_index(doc, output_dir):
        """ Add document index entries for the document
            Apparently this is meant for adding some metadata about the document
        """
        document_index_path = os.path.join(output_dir, 'document_index.json')
        # Load existing document index or create a new one
        document_index = safe_load_json(document_index_path)

        # Add the document ID and its metadata
        doc_id = int(doc['id'])

        flat_keywords = sum(doc['keywords'], [])

        document_index[doc_id] = {
            'title': {'length': len(doc['title']), 'words': doc['title']},
            'text': {'length': len(doc['text']), 'words': doc['text']},
            'keywords': {'length': len(doc['keywords']), 'words': doc['keywords']},
            'unique_terms': {'length': len(set(doc['text'] + doc['title'] + flat_keywords))},
        }

        # Save the updated document index
        safe_save_json(document_index_path, document_index)

    doc['id'] = int(doc['id'])
    doc['all_terms'] = doc['text'] + doc['title'] + sum(doc['keywords'], [])
    uniques, counts = np.unique(doc['all_terms'], return_counts=True)
    uniques = uniques.tolist()
    counts = counts.tolist()
    doc['terms_histogram'] = dict(zip(uniques, counts))

    append_to_term_lexicon(doc, index_path)
    append_to_inverted_index(doc, index_path)
    append_to_document_index(doc, index_path)


def doc_processing(corpus_line, index_path, idx):
    """ Process a single document """

    get_memory_usage(index_path, debug=True, idx=idx)
    doc = json.loads(corpus_line)
    pre_processing(doc)  # tokenizing, stopword removal and stemming
    append_to_structures(doc, index_path)


def indexer(cmd_args):
    """ Main indexer function """

    generate_structures(cmd_args['index'])
    # parallel_index(cmd_args, doc_processing, limit=1000, max_threads=32)
    parallel_index(cmd_args, doc_processing, limit=None, max_threads=32)


def main():
    """ indexes the corpus given the arguments
        - Gets the arguments
        - starts perfomance tracking
        - calls the indexer function
        - later prints the final statistics
    """
    cmd_args = get_indexer_args()
    start_time = time.time()  # Start time for statistics

    print(10*'\n')
    indexer(cmd_args)

    statistics = compute_statistics(start_time, cmd_args['index'])
    print_json(statistics)
    # print_json(statistics)


main()
