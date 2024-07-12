#1) Defining a thread
from fastapi import FastAPI,Query
from fastapi import APIRouter
import threading

output=[]
router = APIRouter()
def myfunc(thread_number:int):
    massage=f"my func called by thread N^{thread_number}"
    output.append(massage)

@router.get("/run1/")
def query(thread_count:int =Query(...,title="Number of threads",ge=1,le=10)):
    global output
    output=[]
    threads=[]
    for i in range(thread_count):
         thread=threading.Thread(target=myfunc,args=(i,))
         threads.append(thread)
         thread.start()
    for thread in threads:
         thread.join()
    return output