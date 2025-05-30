""" Query Processor


## Query Processor

Your implementation must include a `processor.py` file, which will be executed in the previously described environment, as follows:

```bash
python3 processor.py -i <INDEX> -q <QUERIES> -r <RANKER>
```

with the following arguments:

- `-i <INDEX>`: the path to an index file.
- `-q <QUERIES>`: the path to a file with the list of queries to process.
- `-r <RANKER>`: a string informing the ranking function (either “TFIDF” or “BM25”) to be used to score documents for each query.

After processing **each query** (the `-q` argument above), your `processor.py`
implementation must print a `JSON` document to standard output [$^6$][Note_6] with the top
results retrieved for that query according to the following format:

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

The results list for a query must be sorted in reverse document score order and include up to the top 10 results retrieved for that query.

### Query Processing Policies

For each query in the list provided via the `-q` argument, your implementation must pre-process the query, retrieve candidate documents from the given index (the `-i` argument), score these documents according to the chosen ranking model (the `-r` argument), and print the top 10 results using the aforementioned format. In addition to this standard workflow, **your implementation must abide by the following policies**:

1. _Pre-processing Policy_: Your implementation **must pre-process queries with stopword removal and stemming**. This policy should be aligned with the implemented document pre-processing policy for indexing to correctly match queries with documents.
2. _Matching Policy_: For improved efficiency, your implementation **must perform a conjunctive document-at-a-time (DAAT) matching** when retrieving candidate documents.
3. _Scoring Policy_: Your implementation **must provide two scoring functions: TFIDF and BM25**. You are free to experiment with different variants of these functions from the literature.
4. _Parallelization Policy (extra)_: To ensure maximum efficiency, you **may parallelize the query processing across multiple threads**. You may experiment to find an optimal number of threads to maximize your throughput while minimizing the incurred parallelization overhead.

"""
