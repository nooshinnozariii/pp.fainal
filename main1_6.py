#6) Thread synchronization with semaphores
from fastapi import FastAPI, Query
from fastapi import APIRouter
from typing import List
import threading
import time
import random
import logging

router = APIRouter()


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(threadName)s %(levelname)s %(message)s")
output = []
log_lock = threading.Lock()


buffer_semaphore = threading.Semaphore(0)
empty_semaphore = threading.Semaphore(1)

class Producer(threading.Thread):
    def __init__(self, items_to_produce: int):
        super().__init__()
        self.items_to_produce = items_to_produce

    def run(self):
        for _ in range(self.items_to_produce):
            time.sleep(random.uniform(1, 2))  # شبیه‌سازی زمان تولید
            item = random.randint(100, 999)
            empty_semaphore.acquire()
            with log_lock:
                logging.info(f"Producer notify: item number {item}")
                output.append(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {threading.current_thread().name} INFO Producer notify: item number {item}")
            buffer_semaphore.release()

class Consumer(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            buffer_semaphore.acquire()
            with log_lock:
                if len(output) >= 1 and "Producer notify" in output[-1]:
                    last_item = output[-1].split()[-1]
                    logging.info(f"Consumer notify: item number {last_item}")
                    output.append(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {threading.current_thread().name} INFO Consumer notify: item number {last_item}")
            empty_semaphore.release()
            time.sleep(random.uniform(1, 2))  # شبیه‌سازی زمان مصرف

@router.get("/run6/", response_model=List[str])
def process_items(produce_count: int = Query(..., title="Number of items to produce", ge=1)):
    global output
    output = []


    producer = Producer(items_to_produce=produce_count)
    consumers = [Consumer() for _ in range(produce_count)]

    producer.start()
    for consumer in consumers:
        consumer.start()


    producer.join()

    for consumer in consumers:
        consumer.join(timeout=1)

    return output