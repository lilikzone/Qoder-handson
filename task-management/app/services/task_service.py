"""Logika bisnis tugas dengan penyimpanan sementara di memori."""

import logging
from datetime import datetime, timezone
from threading import Lock

from app.models.task import StatusTugas, Task, TaskCreate

logger = logging.getLogger(__name__)


class TaskNotFoundError(Exception):
    """Dilempar ketika tugas dengan ID tertentu tidak ditemukan."""

    def __init__(self, task_id: int) -> None:
        super().__init__(f"Tugas dengan id {task_id} tidak ditemukan")
        self.task_id = task_id


class TaskService:
    """Mengelola operasi CRUD tugas di memori."""

    def __init__(self) -> None:
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1
        self._lock = Lock()

    def create_task(self, data: TaskCreate) -> Task:
        """Membuat tugas baru dan mengembalikannya."""
        with self._lock:
            task = Task(
                id=self._next_id,
                judul=data.judul,
                deskripsi=data.deskripsi,
                waktu_dibuat=datetime.now(timezone.utc),
            )
            self._tasks[task.id] = task
            self._next_id += 1
        logger.info("Tugas %s dibuat", task.id)
        return task

    def list_tasks(self) -> list[Task]:
        """Mengembalikan semua tugas."""
        return list(self._tasks.values())

    def get_task(self, task_id: int) -> Task:
        """Mengembalikan tugas berdasarkan ID."""
        task = self._tasks.get(task_id)
        if task is None:
            raise TaskNotFoundError(task_id)
        return task

    def update_status(self, task_id: int, status: StatusTugas) -> Task:
        """Memperbarui status tugas."""
        task = self.get_task(task_id)
        updated = task.model_copy(update={"status": status})
        self._tasks[task_id] = updated
        logger.info("Status tugas %s diubah menjadi %s", task_id, status.value)
        return updated

    def delete_task(self, task_id: int) -> None:
        """Menghapus tugas berdasarkan ID."""
        self.get_task(task_id)
        del self._tasks[task_id]
        logger.info("Tugas %s dihapus", task_id)


task_service = TaskService()


def get_task_service() -> TaskService:
    """Dependency FastAPI untuk mendapatkan instance TaskService."""
    return task_service
