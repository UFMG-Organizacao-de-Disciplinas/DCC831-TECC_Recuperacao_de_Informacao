""" Module for preprocessing text with NLTK """

import nltk  # Natural Language Toolkit for text processing
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Baixar recursos do NLTK, se necessário
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# Carregar stopwords e stemmer uma vez
STOP_WORDS = set(stopwords.words('english'))
STEMMER = PorterStemmer()


def my_tokenize(text):
    """ Tokenizes a text string into words. Returns a list of words. """
    tokens = word_tokenize(text)  # tokenizar e lowercase
    return tokens


def my_stopwords_removal(token_list):
    """ Removes stopwords from a list of tokens. Returns a list of filtered tokens. """
    filtered_tokens = [word for word in token_list if word.lower()
                       not in STOP_WORDS]
    return filtered_tokens


def my_stemmer(token_list):
    """ Applies stemming to a list of tokens. Returns a list of stemmed tokens. """
    stemmed_tokens = [STEMMER.stem(token) for token in token_list]
    return stemmed_tokens


def preprocess_text(text):
    """ Preprocesses a text string by tokenizing, removing stopwords, and stemming. """
    tokens = my_tokenize(text)
    tokens_sw_removed = my_stopwords_removal(tokens)
    stemmed_tokens = my_stemmer(tokens_sw_removed)
    return stemmed_tokens
