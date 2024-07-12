
from fastapi import FastAPI, Query,APIRouter
from fastapi.responses import JSONResponse
from multiprocessing import Process
import time
import os
import signal

router = APIRouter()

def long_running_task():
    try:
        while True:
            time.sleep(1)
    except:
        pass

@router.get("/run11/", response_class=JSONResponse)
def run_process(duration: int = Query(10)):
    logs = []

    # Create a process
    proc = Process(target=long_running_task, name="Primary Process")
    logs.append(f"Process before execution: {proc} {proc.is_alive()}")

    # Start the process
    proc.start()
    logs.append(f"Process running: {proc} {proc.is_alive()}")

    # Allow the process to run for a bit
    time.sleep(3)

    # Terminate the process
    proc.terminate()
    logs.append(f"Process terminated: {proc} {proc.is_alive()}")

    # Join the process
    proc.join()
    logs.append(f"Process joined: {proc} {proc.is_alive()}")
    logs.append(f"Process exit code: {proc.exitcode}")

    return {"results": logs}
