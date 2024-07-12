from fastapi import FastAPI, Query
from multiprocessing import Process, Manager
from typing import Dict, List
from fastapi import APIRouter

router = APIRouter()

def myFunc(index, return_dict):
    outputs = []
    print(f"calling myFunc from process n°: {index}")
    outputs.append(f"calling myFunc from process n°: {index}")
    for i in range(index):
        print(f"output from myFunc is :{i}")
        outputs.append(f"output from myFunc is :{i}")
    return_dict[index] = outputs

@router.get("/run8")
def run_processes(num_processes: int = Query(..., alias="num")) -> Dict[str, List[str]]:
    manager = Manager()
    return_dict = manager.dict()
    processes = []

    for i in range(num_processes + 1):
        p = Process(target=myFunc, args=(i, return_dict))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
    combined_output = []
    for key in sorted(return_dict.keys()):
        combined_output.extend(return_dict[key])

    return {"results": combined_output}
