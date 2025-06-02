""" ## Query Processor

Your implementation must include a `processor.py` file, which will be executed in the previously
described environment, as follows:

```bash
python3 processor.py -i <INDEX> -q <QUERIES> -r <RANKER>
```

with the following arguments:

- `-i <INDEX>`: the path to an index file.
- `-q <QUERIES>`: the path to a file with the list of queries to process.
- `-r <RANKER>`: a string informing the ranking function (either "TFIDF" or "BM25") to be used to
score documents for each query.

After processing **each query** (the `-q` argument above), your `processor.py` implementation must
print a `JSON` document to standard output [$^6$][Note_6] with the top results retrieved for that
query according to the following format:

- `Query`, the query text;
- `Results`, a list of results.

Each result in the Results list must be represented with the fields:

- `ID`, the respective result ID;
- `Score`, the final document score.

The following example illustrates the required output format for a query:

```json
{
  "Query": "information retrieval",
  "Results": [
    { "ID": "0512698", "Score": 24.2},
    { "ID": "0249777", "Score": 12.4},
    ...
  ]
}
```

[Note_6]: https://en.wikipedia.org/wiki/Standard_streams#Standard_output_(stdout)

The results list for a query must be sorted in reverse document score order and include up to the
top 10 results retrieved for that query.

### Query Processing Policies

For each query in the list provided via the `-q` argument, your implementation must pre-process
the query, retrieve candidate documents from the given index (the `-i` argument), score these
documents according to the chosen ranking model (the `-r` argument), and print the top 10 results
using the aforementioned format. In addition to this standard workflow, **your implementation must
abide by the following policies**:

1. _Pre-processing Policy_: Your implementation **must pre-process queries with stopword removal
and stemming**. This policy should be aligned with the implemented document pre-processing policy
for indexing to correctly match queries with documents.
2. _Matching Policy_: For improved efficiency, your implementation **must perform a conjunctive
document-at-a-time (DAAT) matching** when retrieving candidate documents.
3. _Scoring Policy_: Your implementation **must provide two scoring functions: TFIDF and BM25**.
You are free to experiment with different variants of these functions from the literature.
4. _Parallelization Policy (extra)_: To ensure maximum efficiency, you **may parallelize the
query processing across multiple threads**. You may experiment to find an optimal number of threads
to maximize your throughput while minimizing the incurred parallelization overhead.
"""

import json

from modules.auxiliar import get_processor_args
from modules.preprocessing import preprocess_text
from modules.p_rankers import score_query
# from modules.p_parallelism import parallel_process_queries


def load_index(index_path):
    """ Load the index from the specified path """
    index_files = {'ii': {}, 'di': {}, 'tl': {}}
    with open(index_path + '/inverted_index.json', encoding='utf8') as f:
        index_files['ii'] = json.load(f)
    with open(index_path + '/document_index.json', encoding='utf8') as f:
        index_files['di'] = json.load(f)
    with open(index_path + '/term_lexicon.json', encoding='utf8') as f:
        index_files['tl'] = json.load(f)

    return index_files


def query_process(query, index_files, ranker_name):
    """ Query processing function that preprocesses the query, scores it, and returns results """
    processed_query = preprocess_text(query)

    scores = score_query(processed_query, index_files, ranker_name)
    top_k_scores = scores[:10]  # Get top 10 results

    results = [{"ID": str(docid), "Score": round(score, 2)}
               for docid, score in top_k_scores]

    return results


def monothread_query_process(parallel_load):
    """
    Monothread query processing function that processes queries one by one
    - Reads queries from the file specified in cmd_args['queries']
    - Processes each query using the query_process function
    - Groups results by query and returns a dictionary with the results
    """
    index_files = parallel_load['index_files']
    cmd_args = parallel_load['cmd_args']
    ranker_name = cmd_args['ranker']

    queries_results = []

    with open(cmd_args['queries'], encoding='utf8') as f:
        for line in f:
            query_results = {"Query": "", "Results": []}
            query = line.strip()
            # print(f"Processing query: {query}")  # Debugging output
            if not query:
                continue  # Skip empty lines

            query_results["Query"] = query
            results = query_process(query, index_files, ranker_name)
            query_results["Results"] = results
            queries_results.append(query_results)

    return queries_results


def print_processor_result(queries_results):
    """ Print the results of processed queries in JSON format """

    for query_results in queries_results:
        msg = json.dumps(query_results, indent=2)
        print(msg)


def processor(cmd_args):
    """ Main processor function """
    index_files = load_index(cmd_args['index'])

    parallel_process_load = {
        'index_files': index_files,
        'cmd_args': cmd_args,
        'process': query_process,
        'hyperparameters': {
            'limit': 1000,
            'max_threads': 4
        }
    }

    # query_results = parallel_process_queries(parallel_process_load)
    query_results = monothread_query_process(parallel_process_load)
    return query_results


def main():
    """ PA2 - Query Processor """
    cmd_args = get_processor_args()

    print(10*'\n')
    queries_results = processor(cmd_args)
    print_processor_result(queries_results)


if __name__ == "__main__":
    main()
