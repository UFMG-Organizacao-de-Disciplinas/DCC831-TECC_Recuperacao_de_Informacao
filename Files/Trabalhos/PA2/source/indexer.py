""" Indexer


## Indexer

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
import argparse  # Argument parsing
import os  # File operations
import nltk  # Natural Language Toolkit for text processing
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import psutil  # Process and system utilities for memory management

FORCE_CREATE = True  # Force creation of index files if they already exist


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


def generate_structures(index_path):
    """ Generate the index structures (inverted index, document index, term lexicon) """

    def create_file(file_path):
        """ Create a file if it does not exist """
        if not os.path.exists(file_path) or FORCE_CREATE:
            with open(file_path, 'w', encoding='utf8') as f:
                json.dump({}, f, indent=4)

    def generate_inverted_index(output_dir):
        """ Generate the inverted index """
        # Placeholder for actual implementation
        inverted_index_path = os.path.join(output_dir, 'inverted_index.json')
        create_file(inverted_index_path)

    def generate_document_index(output_dir):
        """ Generate the document index """
        document_index_path = os.path.join(output_dir, 'document_index.json')
        create_file(document_index_path)

    def generate_term_lexicon(output_dir):
        """ Generate the term lexicon """
        term_lexicon_path = os.path.join(output_dir, 'term_lexicon.json')
        create_file(term_lexicon_path)

    generate_inverted_index(index_path)
    generate_document_index(index_path)
    generate_term_lexicon(index_path)


def pre_processing(doc):
    """ Pre-process the document (stopword removal and stemming) """

    def tokenize(doc):
        """ Use NLTK to tokenize the document """
        # Ensure NLTK resources are available
        nltk.download('punkt', quiet=True)

        # Tokenize the document text
        doc['text'] = word_tokenize(doc['text'])
        doc['title'] = word_tokenize(doc['title'])
        doc['keywords'] = [word_tokenize(keyword)
                           for keyword in doc['keywords']]

    def remove_stopwords(doc):
        """ Remove stopwords from the document """

        def get_stopwords():
            """ Get previously defined stopwords """
            nltk.download('stopwords', quiet=True)
            stop_words = set(stopwords.words('english'))
            # with open('source/input/stopwords.json', 'r', encoding='utf8') as f:
            #     stop_words = json.load(f)
            return stop_words

        def remove_stopwords_from_list(word_list, stop_words):
            """ Remove stopwords from a list of words """
            return [word for word in word_list if word.lower() not in stop_words]

        stop_words = get_stopwords()

        doc['text'] = remove_stopwords_from_list(doc['text'], stop_words)
        doc['title'] = remove_stopwords_from_list(doc['title'], stop_words)
        doc['keywords'] = [remove_stopwords_from_list(keywords, stop_words)
                           for keywords in doc['keywords']]

        # print(my_stopwords)

    def stem(doc):
        """ Stem the document using NLTK's english stemmer """

        # Ensure NLTK resources are available
        nltk.download('punkt', quiet=True)

        stemmer = PorterStemmer()

        def stem_list(word_list):
            """ Stem a list of words """
            return [stemmer.stem(word) for word in word_list]

        doc['text'] = stem_list(doc['text'])
        doc['title'] = stem_list(doc['title'])
        doc['keywords'] = [stem_list(keywords) for keywords in doc['keywords']]

    # doc = tokenize(doc)
    tokenize(doc)
    # print("Tokenized document:")
    # print(len(doc['text']), len(doc['title']), list(map(len, doc['keywords'])))

    remove_stopwords(doc)
    # print("Removing stopwords from document:")
    # print(len(doc['text']), len(doc['title']), list(map(len, doc['keywords'])))

    stem(doc)


def append_to_structures(doc, index_path):
    """ Append the processed document to the index structures """

    def append_to_inverted_index(doc, output_dir):
        """ Add inverted index entries for the document
            Only the text field is indexed, title and keywords are not indexed
            Also, only the existance of the term is indexed, not its frequency
        """
        inverted_index_path = os.path.join(output_dir, 'inverted_index.json')

        # Load existing inverted index or create a new one
        if os.path.exists(inverted_index_path):
            with open(inverted_index_path, 'r', encoding='utf8') as f:
                inverted_index = json.load(f)
        else:
            inverted_index = {}

        # Add entries for each term in the document
        id = int(doc['id'])
        for term in doc['text']:
            if term not in inverted_index:
                inverted_index[term] = []
            inverted_index[term].append(id)

        # # Save the updated inverted index
        with open(inverted_index_path, 'w', encoding='utf8') as f:
            json.dump(inverted_index, f, indent=4)

    def append_to_document_index(doc_idx, output_dir):
        """ Add document index entries for the document """

    def append_to_term_lexicon(doc_term_lex, output_dir):
        """ Add term lexicon entries for the document """

    output_dir = os.path.dirname(index_path)

    append_to_inverted_index(doc, output_dir)
    # append_to_document_index(doc, output_dir)
    # append_to_term_lexicon(doc, output_dir)


def doc_processing(doc, mem_limit, index_path):
    """ Process a single document """

    doc = json.loads(doc)

    pre_processing(doc)  # tokenizing, stopword removal and stemming

    append_to_structures(doc, index_path)


def indexer(cmd_args):
    """ Main indexer function """

    generate_structures(cmd_args['index'])

    limit = 2
    idx = 0

    with open(cmd_args['corpus'], 'r', encoding='utf8') as corpus_file:
        for doc in corpus_file:
            if idx >= limit:
                break
            idx += 1
            # doc_processing(doc, cmd_args['memory'], cmd_args['index'])


def main():
    """
        - Gets the arguments
        - starts perfomance tracking
        - calls the indexer function
        - later prints the final statistics
    """
    cmd_args = get_indexer_args()
    start_time = time.time()  # Start time for statistics

    indexer(cmd_args)

    # statistics = compute_statistics(start_time, cmd_args['index'])
    # print_json(statistics)


main()
