from fastapi import FastAPI
from fastapi.routing import APIRouter
from main1_1 import router as main1_1_router
from main1_2 import router as main1_2_router
from main1_3 import router as main1_3_router
from main1_4 import router as main1_4_router
from main1_5 import router as main1_5_router
from main1_6 import router as main1_6_router
from main1_7 import router as main1_7_router

from main2_1 import router as main2_1_router
from main2_2 import router as main2_2_router
from main2_3 import router as main2_3_router
from main2_4 import router as main2_4_router
from main2_5 import router as main2_5_router
from main2_6 import router as main2_6_router
from main2_7 import router as main2_7_router
from main2_8 import router as main2_8_router





app = FastAPI()
app.include_router(main1_1_router, prefix="/api1")
app.include_router(main1_2_router, prefix="/api2")
app.include_router(main1_3_router, prefix="/api3")
app.include_router(main1_4_router, prefix="/api4")
app.include_router(main1_5_router, prefix="/api5")
app.include_router(main1_6_router, prefix="/api6")
app.include_router(main1_7_router, prefix="/api7")

app.include_router(main2_1_router, prefix="/api8")
app.include_router(main2_2_router, prefix="/api9")
app.include_router(main2_3_router, prefix="/api10")
app.include_router(main2_4_router, prefix="/api11")
app.include_router(main2_5_router, prefix="/api12")
app.include_router(main2_6_router, prefix="/api13")
app.include_router(main2_7_router, prefix="/api14")
app.include_router(main2_8_router, prefix="/api15")









if __name__ == "__main__":
    import uvicorn
    uvicorn .run(app, host="0.0.0.1", port=8000)
