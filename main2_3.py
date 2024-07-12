from fastapi import FastAPI, Query,APIRouter
from fastapi.responses import JSONResponse
from threading import Thread
import time

router = APIRouter()

def no_background_process(start: int):
    output = []
    output.append("Starting NO_background_process")
    for i in range(start, start + 5):
        output.append(f"---> {i}")
        time.sleep(1)
    output.append("Exiting NO_background_process")
    return output

def background_process(start: int, result: list):
    output = []
    output.append("Starting background_process")
    for i in range(start, start + 5):
        output.append(f"---> {i % 5}")
        time.sleep(1)
    output.append("Exiting background_process")
    result.extend(output)

@router.get("/run10/")
async def process(start: int = Query(...)):
    result = []
    no_background_output = no_background_process(start)
    result.extend(no_background_output)

    thread = Thread(target=background_process, args=(start, result))
    thread.start()
    thread.join()

    no_background_output = no_background_process(start)
    result.extend(no_background_output)

    return JSONResponse(content={"Primary Output": result})

