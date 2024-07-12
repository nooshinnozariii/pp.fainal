from fastapi import Query,APIRouter
from fastapi.responses import JSONResponse
from threading import Thread, Barrier
import time
import datetime
import random

router = APIRouter()

def racer(name: str, barrier: Barrier, output: list):
    time.sleep(random.uniform(1, 3))  # Simulate time to reach the barrier
    reached_time = datetime.datetime.now().strftime("%a %b %d %H:%M:%S %Y")
    output.append(f"{name} reached the barrier at: {reached_time}")
    barrier.wait()

@router.get("/run7")
async def race():
    barrier = Barrier(3)
    output = ["START RACE!!!!"]

    racers = ["Dewey", "Huey", "Louie"]
    threads = []

    for racer_name in racers:
        thread = Thread(target=racer, args=(racer_name, barrier, output))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    output.append("Race over!")
    return JSONResponse(content={"Primary Output": output})


