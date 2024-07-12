#3) Defining a thread subclass
from fastapi import FastAPI, Query
import threading
import time
import os
from typing import List
from fastapi import APIRouter

router = APIRouter()


output = []


class MyThread(threading.Thread):
    def __init__(self, thread_number: int):
        super().__init__()
        self.thread_number = thread_number

    def run(self):
        global output
        pid = os.getpid()
        output.append(f"---> Thread#{self.thread_number} running, belonging to process ID {pid}")
        time.sleep(1)
        output.append(f"---> Thread#{self.thread_number} over")


@router.get("/run3/", response_model=List[str])
def run_threads(thread_count: int = Query(..., title="Number of threads", ge=1, le=10)) -> List[str]:
    global output
    output = []
    threads = []

    start_time = time.time()

    for i in range(thread_count):
        thread = MyThread(thread_number=i + 1)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    total_time = end_time - start_time

    output.append(f"End\n--- {total_time} seconds ---")

    return output