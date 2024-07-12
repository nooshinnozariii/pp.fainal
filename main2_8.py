from fastapi import APIRouter, Query
from multiprocessing import Pool

router =APIRouter()


def square_number(n):
    return n * n


@router.get("/run15/")
async def compute_squares(start: int = Query(0), end: int = Query(100)):
    numbers = list(range(start, end + 1))
    with Pool(processes=4) as pool:
        result = pool.map(square_number, numbers)

    return {"Pool": result}
