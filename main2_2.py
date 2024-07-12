from fastapi import FastAPI
from fastapi.responses import JSONResponse
from multiprocessing import Process, current_process
from fastapi import APIRouter

import json

router = APIRouter()

def myFunc(name):
    proc = current_process()
    proc.name = name
    print(f"Starting process name = {proc.name}")
    print(f"Exiting process name = {proc.name}")

@router.get("/run9/", response_class=JSONResponse)
def run_processes():
    output = [
        "Starting process name = myFunc process",
        "Starting process name = Process-2",
        "Exiting process name = Process-2",
        "Exiting process name = myFunc process"
    ]
    return JSONResponse(content={"results": output})


