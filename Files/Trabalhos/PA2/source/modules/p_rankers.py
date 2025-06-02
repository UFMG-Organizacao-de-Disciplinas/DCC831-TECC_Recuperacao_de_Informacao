# from heapq import heappush, heappop, heapify
import math
import numpy as np
from modules.auxiliar import print_json


def compute_score(score_info):
    """ Compute the score for a document based on the ranking model
        - score_info: dictionary containing term, tf, doc_id, document_index, lexicon, N, model
    """

    def compute_bm25_score(info, b=0.75, k1=1.2):
        """ Compute BM25 score for a document
            - Needed parameters:
                - Query tokens
                - N = Corpus Size
                - Document
                - df(qi): term frequency in the corpus
                - tf(qi, d): term frequency in the document
                - dl(d): document length
                - avg_dl: average document length in the corpus
                - b, k1: BM25 parameters
        """

        query_terms = info['query_terms']
        inv_index = info['inv_idx']
        doc_id = info['doc_id']
        corpus_size = info['corpus_size']
        dl = info['doc_len']
        avg_dl = info['avg_doc_len']
        query_postings = info['selected_postings']

        score = 0.0
        for term in query_terms:
            corpus_term_freq = len(inv_index.get(term, []))

            # Computing idf (inverse document frequency)
            idf_num = corpus_size - corpus_term_freq + 0.5
            idf_den = corpus_term_freq + 0.5
            idf_div = idf_num / idf_den

            idf = math.log(idf_div)

            # Computing tf (term frequency)
            term_postings = query_postings.get(term, {})
            doc_term_freq = term_postings.get(doc_id, 0)

            tf_num = doc_term_freq * (k1 + 1)
            tf_den = doc_term_freq + (k1 * ((1 - b) + (b * (dl / avg_dl))))

            tf = tf_num / tf_den if tf_den > 0 else 0
            # BM25 score for the term
            score += idf * tf

        # print(f"BM25 score for doc {doc_id}: {score}")

        return score

    def compute_tfidf_score(tfidf_info):
        """ Compute TF-IDF score for a document """

        # inv_index = tfidf_info['inv_idx']
        doc_id = tfidf_info['doc_id']

        query_terms = tfidf_info['query_terms']
        doc_len = tfidf_info['doc_len']
        corpus_len = tfidf_info['corpus_size']

        term_hist = tfidf_info['term_hist']
        query_postings = tfidf_info['selected_postings']

        score = 0.0
        for term in query_terms:
            postings = query_postings.get(term, [])

            doc_term_freq = postings.get(doc_id, 0)

            tf = doc_term_freq / doc_len if doc_len > 0 else 0

            idf = math.log(corpus_len / term_hist.get(term, 1))

            score += tf * idf

        return score

    if score_info['ranker'] == 'BM25':
        return compute_bm25_score(score_info)
    if score_info['ranker'] == 'TFIDF':
        return compute_tfidf_score(score_info)

    return 0.0


def get_query_related_postings(query, inverted_index):
    """ Get the postings related to the terms in the query """
    query_postings = {term: {} for term in query}
    for term in query:
        if term in inverted_index:
            term_postings = inverted_index[term]
            posting_dict = {}
            for doc_id, tf in term_postings:
                posting_dict[doc_id] = tf
            # Convert postings to a dictionary for easier access

            query_postings[term] = posting_dict
        else:
            # If the term is not in the index, return an empty list
            print(f"Oopsie! Term '{term}' not found in the index. 🕵️")

    # if len(query_postings) == len(query):
    #     print('got all query terms in the index!')

    # query_postings.sort(key=lambda x: len(x[1]))
    # Sort postings by the number of documents they appear in (ascending order)
    return query_postings


def get_conjunctive_postings(query_postings):
    """ Get the conjunctive postings for the query terms
        Pseudocode:
        - query_postings: dictionary where keys are terms and values are their postings
            - postings: list of lists [[doc_id, tf], ...]
        - first: get all doc_ids from the first term's postings
        - second: for each subsequent term's postings, keep only those doc_ids
                  that are also in the first term's postings
        - return the updated query_postings with only the common doc_ids and their tf values
    """

    first_term = next(iter(query_postings))
    common_docs = set(query_postings[first_term].keys())

    # conjunctively intersect the postings of the other terms
    for term in query_postings:
        if term != first_term:
            doc_ids = set(query_postings[term].keys())
            common_docs &= doc_ids

    if not common_docs:
        print('No common documents found for the query terms.')
        return query_postings

    conjunctive_postings = {term: {} for term in query_postings}

    for term in query_postings:
        for common_doc in common_docs:
            tf = query_postings[term].get(common_doc, 0)
            conjunctive_postings[term][common_doc] = tf

    return conjunctive_postings


def run_daat(query, index_files, postings_to_score, ranker):
    """ Run the Document-at-a-Time (DAAT) algorithm to score documents
        Args:
            - query: preprocessed query (list of terms)
            - index_files: dictionary with inverted index, document index, and lexicon
                - inverted_index: dictionary with terms as keys and postings as values
                    - postings: list of lists [[doc_id, tf], ...]
                - document_index: dictionary with document IDs and their metadata
                    - id: {text: term list, title: term list, keywords: term list, unique_terms: length: int}
                - lexicon: dictionary with terms and their metadata
                    - term_hist: dictionary with term frequencies in the corpus
                    - term2id: dictionary mapping terms to their IDs
            - postings_to_score: dictionary with terms from the query and their postings
            - ranker: 'TFIDF' or 'BM25'
        Logic: run the DAAT algorithm to score documents based on the query terms
    """
    # print_json(postings_to_score)

    individual_doc_ids = set()

    for _, postings in postings_to_score.items():
        individual_doc_ids.update(postings.keys())
    individual_doc_ids = sorted(individual_doc_ids)

    doc_idx = index_files['di']

    query_terms = list(postings_to_score.keys())
    inv_idx = index_files['ii']

    corpus_size = len(doc_idx)

    # Calculate average document length
    total_length = sum(doc['unique_terms']['length']
                       for doc in doc_idx.values())
    avg_doc_len = total_length / corpus_size if corpus_size > 0 else 0

    # scores_dict = {}
    scores_tuples = []

    for doc_id in individual_doc_ids:
        # This should be a kind of daat, but i'm not sure if it is.
        # Id kinda goes a document at a time tho.

        doc_dict = doc_idx.get(doc_id, {})
        doc_len = doc_dict.get('unique_terms', 0)

        scoring_payload = {
            'query_terms': query_terms,
            'inv_idx': inv_idx,
            'doc_id': doc_id,
            'corpus_size': corpus_size,
            'doc_len': doc_len,
            'avg_doc_len': avg_doc_len,
            'ranker': ranker,
            'selected_postings': postings_to_score,
            'term_hist': index_files['tl']['terms_histogram']
        }
        score = compute_score(scoring_payload)
        # scores_dict[doc_id] = score
        scores_tuples.append((doc_id, score))

    # Sort the scores in descending order
    scores_tuples.sort(key=lambda x: x[1], reverse=True)
    # print(f"Scores for query '{query}': {scores_tuples}")

    return scores_tuples


def document_at_a_time(query, index_files, ranker):
    """ Process one document at a time to retrieve its score
        - Keep one pointer for each term in the query
    """
    inverted_index = index_files['ii']

    query_postings = get_query_related_postings(query, inverted_index)
    if not query_postings:
        return []

    postings_to_score = get_conjunctive_postings(query_postings)

    # print(f"Postings to score: {postings_to_score}")

    scores = run_daat(query, index_files, postings_to_score, ranker)
    return scores


def score_query(query, index_files, ranker='BM25'):
    """ Score a query using the specified ranker.
        - query: preprocessed query (list of terms)
        - index_files: dictionary with inverted index, document index, and lexicon
        - ranker: 'TFIDF' or 'BM25'
    """
    print(5*'\n')
    scores = document_at_a_time(query, index_files, ranker)
    print(5*'\n')

    return scores
