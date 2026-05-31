import asyncio
from contextlib import asynccontextmanager, suppress

from fastapi import FastAPI

from app.cashback.application.kafka_listener import consume_kafka
from app.cashback.application.router import cashback_router
from app.cashback.infrastructure.impl_config import get_cashback_service
from app.config.db_engine import create_db_and_tables
from app.config.kafka import KAFKA_CONSUMER


@asynccontextmanager
async def lifespan(_app: FastAPI):
    create_db_and_tables()
    task = asyncio.create_task(consume_kafka(KAFKA_CONSUMER, get_cashback_service()))

    yield

    assert task.cancel()

    with suppress(asyncio.CancelledError):
        await task

    KAFKA_CONSUMER.close()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def health():
    return {"status": "ok"}


app.include_router(cashback_router)
