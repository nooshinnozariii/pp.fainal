#5) Thread synchronization with RLock
from fastapi import FastAPI, Query
from fastapi import APIRouter
import threading
import time
from typing import List

router = APIRouter()

output = []
rlock = threading.RLock()

class ItemHandler(threading.Thread):
    def __init__(self, add_count: int, remove_count: int):
        super().__init__()
        self.add_count = add_count
        self.remove_count = remove_count

    def run(self):
        global output
        while self.remove_count > 0:
            with rlock:
                output.append(f"REMOVED one item -->{self.remove_count - 1} item to REMOVE")
            self.remove_count -= 1
            time.sleep(0.1)  # Sleep to simulate work and make output clearer
        while self.add_count > 0:
            with rlock:
                output.append(f"ADDED one item -->{self.add_count - 1} item to ADD")
            self.add_count -= 1
            time.sleep(0.1)  # Sleep to simulate work and make output clearer

@router.get("/run5/", response_model=List[str])
def handle_items(add_count: int = Query(..., title="Number of items to add", ge=0),
                 remove_count: int = Query(..., title="Number of items to remove", ge=0)) -> List[str]:
    global output
    output = [f"N° {add_count} items to ADD", f"N° {remove_count} items to REMOVE"]

    handler = ItemHandler(add_count, remove_count)
    handler.start()
    handler.join()

    return output