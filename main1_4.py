#4) Thread synchronization with a lock
from fastapi import FastAPI, Query
import threading
import time
from fastapi import APIRouter
import json
import os

router = APIRouter()

lock = threading.Lock()
output = []
start_time = time.time()

@router.get("/run4", response_model=dict)
def run_threads(thread_count: int = Query(..., title="Number of threads", ge=1)):
    global output, start_time
    output = []
    start_time = time.time()
    threads = []

    def thread_function(thread_num):
        with lock:
            pid = os.getpid()
            output.append(f"---> Thread#{thread_num} running, belonging to process ID {pid}")
            time.sleep(1)  # Simulating some work
            output.append(f"---> Thread#{thread_num} over")

    # Creating and starting threads
    for i in range(1, thread_count + 1):
        thread = threading.Thread(target=thread_function, args=(i,))
        threads.append(thread)
        thread.start()

    # Waiting for all threads to finish
    for thread in threads:
        thread.join()

    # Adding end message and calculating total time
    output.append("End")
    end_time = time.time()
    total_time = end_time - start_time
    output.append(f"--- {total_time} seconds ---")

    return {"Primary Output": output}

