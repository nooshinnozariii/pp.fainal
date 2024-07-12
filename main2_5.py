from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from multiprocessing import Process, Manager

router = APIRouter()

class MyProcess(Process):
    def __init__(self, name, return_list):
        super().__init__()
        self.name = name
        self.return_list = return_list

    def run(self):
        self.return_list.append(f"called run method by {self.name}")

@router.get("/run12", response_class=JSONResponse)
def run_processes(count: int = Query(10)):
    manager = Manager()
    return_list = manager.list()

    processes = []
    for i in range(1, count + 1):
        proc = MyProcess(name=f"MyProcess-{i}", return_list=return_list)
        processes.append(proc)
        proc.start()

    for proc in processes:
        proc.join()

    return {"results": list(return_list)}