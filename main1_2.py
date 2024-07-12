#2) Determining the current thread
from fastapi import FastAPI, Query
from fastapi import APIRouter
import threading
from typing import List

router = APIRouter()

output = []

def function_A():
    global output
    output.append("function_A--> starting")
    output.append("function_A--> exiting")
def function_B():
    global output
    output.append("function_B--> starting")
    output.append("function_B--> exiting")


def function_C():
    global output
    output.append("function_C--> starting")
    output.append("function_C--> exiting")


@router.get("/run2/", response_model=List[str])
def execute_functions(thread_count: int = Query(..., title="Number of threads", ge=1, le=3)) -> List[str]:
    global output
    output = []
    threads = []

    functions = [function_A, function_B, function_C]

    if thread_count > len(functions):
        thread_count = len(functions)

    for i in range(thread_count):
        thread = threading.Thread(target=functions[i])
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return output