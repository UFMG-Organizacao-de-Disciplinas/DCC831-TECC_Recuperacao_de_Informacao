""" Get arguments """


def get_indexer_args():
    """ Return a dictionary of the needed arguments, those being:
        -m <MEMORY> : Memory in MB
        -c <CORPUS> : Corpus path
        -i <INDEX>  : Index path
    """
    import argparse

    parser = argparse.ArgumentParser(description="Indexer arguments")
    parser.add_argument("-m", "--memory", type=int,
                        required=True, help="Memory in MB")
    parser.add_argument("-c", "--corpus", type=str,
                        required=True, help="Corpus path")
    parser.add_argument("-i", "--index", type=str,
                        required=True, help="Index path")

    args = parser.parse_args()

    args_dict = vars(args)


get_indexer_args()
