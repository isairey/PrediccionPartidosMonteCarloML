from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.predictions import router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
def root():
    return {
        "message":
        "Football Predictor API"
    }