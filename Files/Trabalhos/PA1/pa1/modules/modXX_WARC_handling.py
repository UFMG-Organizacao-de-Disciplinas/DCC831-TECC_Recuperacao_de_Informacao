""" WARCs """

# Importing my modules

from modules.mod02_utils import constants

# Importing libraries

from warcio.warcwriter import WARCWriter # GPT is helping me with WARCing
from warcio.statusandheaders import StatusAndHeaders
from warcio.archiveiterator import ArchiveIterator # Needed for reading WARC files
import gzip # Needed for reading WARC files
from io import BytesIO # GPT is helping me with WARCing
from threading import Lock

""" store_warc: Stores the parsed URL in a WARC file. """
warc_lock = Lock()  # Lock for thread-safe writing to WARC files

def store_warc(parsed_url, index, warc_file_saving_method='ab', is_compressed=True):
    """ Stores the parsed URL in a WARC file. """

    def get_protocol_version(version):
        """ Returns the protocol version used in the response. """
        protocol  = f'unknown {version}'
        if version == 10:
            protocol = 'HTTP/1.0'
        elif version == 11:
            protocol = 'HTTP/1.1'
        elif version == 20:
            protocol = 'HTTP/2.0'
        return protocol

    output_path = f'WARCs/output_{index:03}.warc'
    if is_compressed:
        output_path += '.gz'

    headers = StatusAndHeaders(
        statusline=str(parsed_url['Status_Code']),
        headers={},
        # headers=parsed_url['Headers'].items(), # Mais completo, mas poluído.
        protocol=get_protocol_version(parsed_url['Version']),
    )

    # print_json(parsed_url['HTML'])
    # ab = Append and Binary mode.
    with open(output_path, warc_file_saving_method) as output:
        # gzip = True makes it automatically compressed.
        writer = WARCWriter(output, gzip=is_compressed)
        record = writer.create_warc_record(
            uri=parsed_url['URL'],
            record_type='response',
            payload=BytesIO(parsed_url['HTML'].encode('utf-8')),
            # payload=parsed_url['Raw'],
            http_headers=headers,
        )
        writer.write_record(record)


def store_warcs(scraping, warc_size=1000, debug_time_elapsed=None):
    """ Stores the parsed URLs in a WARC file. """
    with warc_lock:
        content = scraping['content']
        index = scraping['count'] // warc_size
        
        debug_time_elapsed()
        
        for parsed_url in content.values():
            store_warc(parsed_url, index, 'ab')


""" read_warc: Reads the WARC file and prints its contents. """

def read_warc_zipped_file(warc_path):
    """ Reads and prints the WARC file contents. """
    with open(warc_path, 'rb') as stream:
        if warc_path.endswith('.gz'):
            stream = gzip.GzipFile(fileobj=stream)

        for record in ArchiveIterator(stream):
            if record.rec_type == 'response':
                uri = record.rec_headers.get_header('WARC-Target-URI')
                payload = record.content_stream().read()
                print(f"URI: {uri}")
                print(f"Payload: {payload[:500]}...")  # Show first 500 bytes
                print("-" * 50)

# read_warc_zipped_file('output.warc.gz')
