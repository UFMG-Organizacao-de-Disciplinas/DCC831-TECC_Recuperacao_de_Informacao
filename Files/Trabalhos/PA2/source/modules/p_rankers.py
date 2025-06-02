from heapq import heappush, heappop, heapify
import math
import numpy as np


def compute_score(score_info):
    """ Compute the score for a document based on the ranking model
        - score_info: dictionary containing term, tf, doc_id, document_index, lexicon, N, model
    """

    def compute_bm25_score(info, b=0.75, k1=1.2):
        """ Compute BM25 score for a document """
        term = info['term']
        tf = info['tf']
        doc_id = info['doc_id']
        document_index = info['document_index']
        lexicon = info['lexicon']
        index_size = info['index_size']

        # Get the document length and average document length
        doc_length = len(document_index[doc_id]['terms'])
        avg_doc_length = np.mean([len(doc['terms'])
                                 for doc in document_index.values()])

        # Get the document frequency of the term
        doc_freq = lexicon['term_hist'][term]

        # Calculate BM25 score
        idf = math.log((index_size - doc_freq + 0.5) / (doc_freq + 0.5) + 1)

        num = idf * (tf * (k1 + 1))
        denom = tf + k1 * (1 - b + b * (doc_length / avg_doc_length))

        score = num / denom

        return score

    def compute_tfidf_score(info):
        """ Compute TF-IDF score for a document """
        term = info['term']
        tf = info['tf']
        # doc_id = info['doc_id']
        document_index = info['document_index']
        lexicon = info['lexicon']

        # Get the document frequency of the term
        doc_freq = lexicon['term_hist'][term]
        index_size = len(document_index)

        # Calculate TF-IDF score
        idf = math.log(index_size / (doc_freq + 1))
        score = tf * idf
        return score

    if score_info['model'] == 'BM25':
        return compute_bm25_score(score_info)
    if score_info['model'] == 'TFIDF':
        return compute_tfidf_score(score_info)

    return 0.0


def get_relevant_postings(query, inverted_index):
    """ Get the postings related to the terms in the query """
    query_postings = []
    for term in query:
        if term in inverted_index:
            term_postings = inverted_index[term]
            query_postings.append((term, term_postings))

    query_postings.sort(key=lambda x: len(x[1]))
    # Sort postings by the number of documents they appear in (ascending order)
    return query_postings


def slide_daat(query, index, k):
    """ DAAT algorithm from slides """
    results = heapify(k)
    targets = {docid for term in query for docid in index[term]}
    lists = [index[term] for term in query]
    for target in targets:
        score = 0
        for postings in lists:
            for (docid, weight) in postings:
                if docid == target:
                    score += weight
        results.add(target, score)
    return results


def get_daat_scores(query_postings):
    """ Calculate scores for each document based on the query terms """
    pointers = [0] * len(query_postings)
    scores = {}

    while True:
        current_docids = []
        for i, (term, plist) in enumerate(query_postings):
            pointer_exceeds_postings_size = pointers[i] >= len(plist)
            if not pointer_exceeds_postings_size:
                # Get the current document ID base on the pointer position
                doc_id = plist[pointers[i]][0]
                current_docids.append(doc_id)
            else:
                # Hard stop if any pointer exceeds the postings size
                # Could be improved
                return scores

        if len(set(current_docids)) == 1:
            doc_id = str(current_docids[0])  # converte para string
            score = 0

            for i, (term, plist) in enumerate(query_postings):
                _, tf = plist[pointers[i]]
                score_info = {
                    'term': term,
                    'tf': tf,
                    'doc_id': doc_id,
                    'document_index': document_index,
                    'lexicon': lexicon,
                    'index_size': len(document_index),
                    'model': model
                }
                score += compute_score(score_info)
                pointers[i] += 1

            scores[doc_id] = score

        else:
            min_docid = min(current_docids)
            for i, _ in enumerate(query_postings):
                first_cond = pointers[i] < len(query_postings[i][1])
                second_cond = query_postings[i][1][pointers[i]][0] == min_docid
                if first_cond and second_cond:
                    pointers[i] += 1


def document_at_a_time(query, inverted_index):
    """ Process one document at a time to retrieve its score
        - Keep one pointer for each term in the query
    """

    query_postings = get_relevant_postings(query, inverted_index)
    if not query_postings:
        return {}

    scores = get_daat_scores()

    return scores


def score_query(query, index_files, ranker='BM25'):
    """
    Score a query using the specified ranker.
    - query: preprocessed query (list of terms)
    - index_files: dictionary with inverted index, document index, and lexicon
    - ranker: 'TFIDF' or 'BM25'
    """
    inverted_index = index_files['ii']
    document_index = index_files['di']
    lexicon = index_files['lex']

    term2id = lexicon['term2id']
    term_hist = lexicon['term_hist']
    index_size = len(document_index)

    scores = document_at_a_time(query, inverted_index)

    return scores
