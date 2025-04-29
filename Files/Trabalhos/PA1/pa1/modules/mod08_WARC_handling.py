# """ WARCs """

# # Importing my modules

from modules.mod00_debugging import debug_time_elapsed

# # Importing Suggested libraries

# # Importing my needed libraries

from warcio.warcwriter import WARCWriter # GPT is helping me with WARCing
from warcio.statusandheaders import StatusAndHeaders
from warcio.archiveiterator import ArchiveIterator # Needed for reading WARC files
import gzip # Needed for reading WARC files
from io import BytesIO # GPT is helping me with WARCing
from threading import Lock
import os # Assure the directory exists
from concurrent.futures import ThreadPoolExecutor # For multithreading

# # Global variables

warc_lock = Lock() # Global lock for thread-safe WARC file operations this ensures multiple threads don't write to the same WARC file simultaneously
warc_executor = ThreadPoolExecutor(max_workers=1) # Thread pool for parallel WARC writing

# # WARC Store and Read functions


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

def store_warc(warc_file, parsed_url, is_compressed, index, storage_index):
    """ Stores the parsed URL in a WARC file. """

    headers = StatusAndHeaders(
        statusline=str(parsed_url['Status_Code']),
        headers={},
        # headers=parsed_url['Headers'].items(), # Mais completo, mas poluído.
        protocol=get_protocol_version(parsed_url['Version']),
    )

    # ab = Append and Binary mode.
    # gzip = True makes it automatically compressed.
    writer = WARCWriter(warc_file, gzip=is_compressed)
    record = writer.create_warc_record(
        uri=parsed_url['URL'],
        # uri=f'{storage_index:03}_{index:03}_'+parsed_url['URL'],
        record_type='response',
        payload=BytesIO(parsed_url['HTML'].encode('utf-8')),
        # payload=parsed_url['Raw'],
        http_headers=headers,
    )
    writer.write_record(record)


def warc_as_you_go(scraping, parsed_url, is_compressed=False):
    """ Stores the parsed URLs in a WARC file. """
    # print(">>> Storing WARC file <<<")
    
    # debug_time_elapsed()

    with warc_lock:
        scraping['stored'] += 1  # Increment the stored count
        scraping['stored_urls'].add(parsed_url['URL'])  # Add the URL to the set of stored URLs

        # index = (scraping['stored'] // (scraping['constants']['WARC_SIZE'] + 1))
        index = ((scraping['stored'] - 1) // scraping['constants']['WARC_SIZE']) + 1
        output_path = f'WARCs/output_{index:03}.warc'

        if is_compressed:
            output_path += '.gz'

        warc_file_saving_method = 'ab'

        os.makedirs('WARCs', exist_ok=True)  # Create the directory if it doesn't exist
        
        with open(output_path, warc_file_saving_method) as warc_file:
            store_warc(warc_file, parsed_url, is_compressed, index, scraping['stored'])
    

def store_warcs(scraping, is_compressed=False):
    """ Stores the parsed URLs in a WARC file. """
    print(f">>> Storing WARC file for {scraping['count']} pages... <<<")
    debug_time_elapsed()
    
    with warc_lock:
        scraping['stored'] += 1  # Increment the stored count
        print(f"PRE {len(scraping['content'])} pages in WARC file...")
        batch = scraping['content'].copy()  # Copy the content to avoid modifying it while iterating
        print(f"POS {len(batch)} pages in WARC file...")
        scraping['content'].clear()  # Clear the content after copying

        storage_index = scraping['stored']

        output_path = f'WARCs/output_{storage_index:03}.warc'
        if is_compressed:
            output_path += '.gz'

        warc_file_saving_method = 'ab'
        
        os.makedirs('WARCs', exist_ok=True)  # Create the directory if it doesn't exist
        with open(output_path, warc_file_saving_method) as warc_file:
            print(len(batch))
            index = 1
            for parsed_url in batch.values():
                print(f"\tStoring {storage_index}:{index}/{len(batch)} pages in WARC file...")
                store_warc(warc_file, parsed_url, is_compressed, index, scraping['stored'])
                index += 1

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
