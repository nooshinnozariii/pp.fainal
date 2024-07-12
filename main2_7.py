from fastapi import APIRouter
import multiprocessing as mp
from datetime import datetime

router= APIRouter()


def test_with_barrier(barrier, queue, label):
    barrier.wait()
    now = datetime.now()
    queue.put((label, f"process {label} - test_with_barrier ----> {now}"))


def test_without_barrier(queue, label):
    now = datetime.now()
    queue.put((label, f"process {label} - test_without_barrier ----> {now}"))


@router.get("/run14/")
async def process_data():
    manager = mp.Manager()
    queue = manager.Queue()
    barrier = mp.Barrier(2)

    p4 = mp.Process(target=test_without_barrier, args=(queue, 'p4'))
    p3 = mp.Process(target=test_without_barrier, args=(queue, 'p3'))
    p1 = mp.Process(target=test_with_barrier, args=(barrier, queue, 'p1'))
    p2 = mp.Process(target=test_with_barrier, args=(barrier, queue, 'p2'))

    p4.start()
    p3.start()
    p4.join()
    p3.join()

    p1.start()
    p2.start()
    p1.join()
    p2.join()

    output = []
    while not queue.empty():
        output.append(queue.get()[1])

    # Ensure the output order is as specified: p4, p3, p1, p2
    output.sort(key=lambda x: ('p4' in x, 'p3' in x, 'p1' in x, 'p2' in x))

    return {"output": output}


