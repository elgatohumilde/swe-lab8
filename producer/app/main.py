from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config.db_engine import create_db_and_tables
from app.orders.application.router import orders_router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def health():
    return {"status": "ok"}


app.include_router(orders_router)
