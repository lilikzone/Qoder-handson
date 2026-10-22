"""Titik awal aplikasi Task Management API."""

import logging

from fastapi import FastAPI

from app.routes.tasks import router as tasks_router

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Task Management API",
    description="Demo REST API manajemen tugas untuk Workshop Qoder AI",
    version="1.0.0",
)
app.include_router(tasks_router)


@app.get("/", tags=["health"])
def health_check() -> dict[str, str]:
    """Memeriksa apakah API berjalan."""
    return {"status": "ok"}
