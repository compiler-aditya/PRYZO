"""PRYZO Backend — FastAPI entry point."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import init_db
from routers import hunt, dashboard, identify, agent

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    logging.getLogger(__name__).info("PRYZO backend started")
    yield
    logging.getLogger(__name__).info("PRYZO backend shutting down")


app = FastAPI(
    title="PRYZO",
    description="AI Deal Hunter That Never Sleeps",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(hunt.router)
app.include_router(dashboard.router)
app.include_router(identify.router)
app.include_router(agent.router)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "pryzo"}
