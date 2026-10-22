"""Titik awal aplikasi Task Management API (starter workshop)."""

from fastapi import FastAPI

app = FastAPI(title="Task Management API", version="0.1.0")


@app.get("/", tags=["health"])
def health_check() -> dict[str, str]:
    """Memeriksa apakah API berjalan."""
    return {"status": "ok"}
