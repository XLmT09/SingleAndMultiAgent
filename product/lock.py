# shared_lock.py
import threading

""" Shared flag to be used between the main and path_find generation thread.
The main thread was trying to get a the new visited and path list too
early, i.e path find thread didn't have time to generate the data. This was
leading to a race condition where the main thread was using data which it
had already executed. With this flag the main thread will have to wait or
skip until generation is complete."""
visited_and_path_data_flag = threading.Event()
