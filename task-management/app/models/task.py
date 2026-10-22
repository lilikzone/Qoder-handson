"""Model Pydantic untuk data tugas."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class StatusTugas(str, Enum):
    """Pilihan status tugas."""

    BELUM_MULAI = "belum_mulai"
    PROSES = "proses"
    SELESAI = "selesai"


class TaskCreate(BaseModel):
    """Data masukan untuk membuat tugas baru."""

    model_config = ConfigDict(str_strip_whitespace=True)

    judul: str = Field(..., min_length=1, max_length=100)
    deskripsi: str | None = Field(default=None, max_length=500)


class TaskStatusUpdate(BaseModel):
    """Data masukan untuk memperbarui status tugas."""

    status: StatusTugas


class Task(BaseModel):
    """Representasi tugas yang dikembalikan oleh API."""

    id: int
    judul: str
    deskripsi: str | None = None
    status: StatusTugas = StatusTugas.BELUM_MULAI
    waktu_dibuat: datetime
