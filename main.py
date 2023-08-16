"""
(venv) C:\Python\FastAPI-Email-Payment-AWS> uvicorn main:app --reload
- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from resources.routes import api_router
from db import database

origins = [
    "http://localhost",
    "http://localhost:4200"
]

app = FastAPI()

app.include_router(api_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
async def root():
    return {"message": "Hellow World"}