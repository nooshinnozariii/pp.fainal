from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from multiprocessing import Process, Queue, Manager
import random
import time

router = APIRouter()

def producer(queue: Queue, output: list, n: int):
    for _ in range(n):
        item = random.randint(1, 1000)
        queue.put(item)
        output.append(f"Process Producer : item {item} appended to queue producer-1")
        output.append(f"The size of queue is {queue.qsize()}")
        time.sleep(random.uniform(0.1, 0.5))

def consumer(queue: Queue, output: list, n: int):
    for _ in range(n):
        if not queue.empty():
            item = queue.get()
            output.append(f"Process Consumer : item {item} popped from by consumer-2")
            if queue.qsize() > 0:
                output.append(f"The size of queue is {queue.qsize()}")
        else:
            break
        time.sleep(random.uniform(0.1, 0.5))
    output.append("the queue is empty")

@router.get("/run13/")
async def process(n: int = Query(...)):
    manager = Manager()
    queue = Queue()
    output = manager.list()  # Shared list for processes

    producer_process = Process(target=producer, args=(queue, output, n))
    consumer_process = Process(target=consumer, args=(queue, output, n))

    producer_process.start()
    consumer_process.start()

    producer_process.join()
    consumer_process.join()

    return JSONResponse(content={"Primary Output": list(output)})

