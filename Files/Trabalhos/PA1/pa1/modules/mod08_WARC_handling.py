# """ WARCs """

# # Importing my modules

# from modules.mod00_debugging import debug_time_elapsed

# # Importing Suggested libraries

# # Importing my needed libraries

# from warcio.warcwriter import WARCWriter # GPT is helping me with WARCing
# from warcio.statusandheaders import StatusAndHeaders
from warcio.archiveiterator import ArchiveIterator # Needed for reading WARC files
import gzip # Needed for reading WARC files
# from io import BytesIO # GPT is helping me with WARCing
# from threading import Lock
# import os # Assure the directory exists
# from concurrent.futures import ThreadPoolExecutor, as_completed # For multithreading

# # Global variables

# warc_lock = Lock() # Global lock for thread-safe WARC file operations this ensures multiple threads don't write to the same WARC file simultaneously
# warc_executor = ThreadPoolExecutor(max_workers=1) # Thread pool for parallel WARC writing

# # WARC Store and Read functions


# def get_protocol_version(version):
#     """ Returns the protocol version used in the response. """
#     protocol  = f'unknown {version}'
#     if version == 10:
#         protocol = 'HTTP/1.0'
#     elif version == 11:
#         protocol = 'HTTP/1.1'
#     elif version == 20:
#         protocol = 'HTTP/2.0'
#     return protocol

# def store_warc(warc_file, parsed_url, is_compressed):
#     """ Stores the parsed URL in a WARC file. """

#     headers = StatusAndHeaders(
#         statusline=str(parsed_url['Status_Code']),
#         headers={},
#         # headers=parsed_url['Headers'].items(), # Mais completo, mas poluído.
#         protocol=get_protocol_version(parsed_url['Version']),
#     )

#     # ab = Append and Binary mode.
#     # gzip = True makes it automatically compressed.
#     writer = WARCWriter(warc_file, gzip=is_compressed)
#     record = writer.create_warc_record(
#         uri=parsed_url['URL'],
#         record_type='response',
#         payload=BytesIO(parsed_url['HTML'].encode('utf-8')),
#         # payload=parsed_url['Raw'],
#         http_headers=headers,
#     )
#     writer.write_record(record)


# def store_warcs(scraping, is_compressed=False):
#     """ Stores the parsed URLs in a WARC file. """
#     print(f">>> Storing WARC file for {scraping['count']} pages... <<<")
#     debug_time_elapsed()
    
#     with warc_lock:
#         scraping['stored'] += 1  # Increment the stored count
#         print(f"PRE {len(scraping['content'])} pages in WARC file...")
#         batch = scraping['content'].copy()  # Copy the content to avoid modifying it while iterating
#         print(f"POS {len(batch)} pages in WARC file...")
#         scraping['content'].clear()  # Clear the content after copying

#         storage_index = scraping['stored']

#         output_path = f'WARCs/output_{storage_index:03}.warc'
#         if is_compressed:
#             output_path += '.gz'

#         warc_file_saving_method = 'ab'
        
#         os.makedirs('WARCs', exist_ok=True)  # Create the directory if it doesn't exist
#         with open(output_path, warc_file_saving_method) as warc_file:
#             print(len(batch))
#             index = 1
#             for parsed_url in batch.values():
#                 print(f"\tStoring {storage_index}:{index}/{len(batch)} pages in WARC file...")
#                 store_warc(warc_file, parsed_url, is_compressed)
#                 index += 1

# # Parallel WARC writing function

# """
# Parallel WARC writing function using ThreadPoolExecutor.

# - Receives a scraping object and a boolean indicating if the WARC file should be compressed.
# - Uses a lock to ensure thread-safe writing to the WARC file.
# - Creates a batch of parsed URLs to write to the WARC file.
# - Calls a thread pool executor to write the WARC file in parallel.
# - In the thread:
#     - Stores the parsed URLs in a WARC file.
# """

# def parallel_store_warcs(scraping, is_compressed=False):
#     """ Stores the parsed URLs in a WARC file in parallel. """
#     print(f">>> Storing WARC file for {scraping['count']} pages... <<<")
#     debug_time_elapsed()

#     with warc_lock:
#         scraping['stored'] += 1  # Increment the stored count
#         batch = scraping['content'].copy()  # Copy the content to avoid modifying it while iterating
#         scraping['content'].clear()  # Clear the content after copying

#         storage_index = scraping['stored']

#         output_path = f'WARCs/output_{storage_index:03}.warc'
#         if is_compressed:
#             output_path += '.gz'

#         os.makedirs('WARCs', exist_ok=True)  # Create the directory if it doesn't exist

#         future = warc_executor.submit(store_warc, output_path, batch, is_compressed)
#         return future    

import os
from threading import Lock
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from warcio.warcwriter import WARCWriter
from warcio.statusandheaders import StatusAndHeaders

# ————————————————
# Global WARC‐writing machinery
# ————————————————

# Lock to protect shared state during snapshot
warc_lock = Lock()

# Single‐threaded executor for writing WARC files
warc_executor = ThreadPoolExecutor(max_workers=1)

def get_protocol_version(version: int) -> str:
    """Returns the HTTP protocol string for a given numeric version."""
    if version == 10:
        return 'HTTP/1.0'
    elif version == 11:
        return 'HTTP/1.1'
    elif version == 20:
        return 'HTTP/2.0'
    else:
        return f'unknown {version}'

def store_warc(warc_file, parsed_url: dict, is_compressed: bool):
    """Write a single parsed_url as one record into an open WARCWriter."""
    headers = StatusAndHeaders(
        statusline=str(parsed_url['Status_Code']),
        headers={},
        protocol=get_protocol_version(parsed_url['Version']),
    )
    writer = WARCWriter(warc_file, gzip=is_compressed)
    record = writer.create_warc_record(
        uri=parsed_url['URL'],
        record_type='response',
        payload=BytesIO(parsed_url['HTML'].encode('utf-8')),
        http_headers=headers,
    )
    writer.write_record(record)

def write_warc_batch(batch: dict, storage_index: int, is_compressed: bool = False):
    """
    Writes an entire batch of parsed_url dicts into output_{storage_index:03}.warc[.gz].
    This function runs inside the warc_executor.
    """
    dirname = 'WARCs'
    os.makedirs(dirname, exist_ok=True)
    output_path = os.path.join(dirname, f'output_{storage_index:03}.warc')
    if is_compressed:
        output_path += '.gz'

    with open(output_path, 'ab') as warc_file:
        for parsed_url in batch.values():
            store_warc(warc_file, parsed_url, is_compressed)

def schedule_warc_write(batch: dict, storage_index: int, is_compressed: bool = False):
    """
    Submit a write_warc_batch job to the dedicated executor.
    """
    warc_executor.submit(write_warc_batch, batch, storage_index, is_compressed)

def parallel_store_warcs(scraping: dict, is_compressed: bool = False):
    """
    Snapshot the current scraping['content'], clear it, bump stored counter,
    and schedule the batch to be written in background.
    """
    with warc_lock:
        batch = scraping['content'].copy()
        scraping['content'].clear()
        scraping['stored'] += 1
        idx = scraping['stored']

    # ensure directory exists before scheduling
    os.makedirs('WARCs', exist_ok=True)
    schedule_warc_write(batch, idx, is_compressed)

# ————————————————
# At end of your program (after all scraping):
# ————————————————

# Wait for any pending WARC writes to finish before exiting
warc_executor.shutdown(wait=True)

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
