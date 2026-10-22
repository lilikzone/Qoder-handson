"""Endpoint REST API untuk manajemen tugas."""

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.models.task import Task, TaskCreate, TaskStatusUpdate
from app.services.task_service import TaskNotFoundError, TaskService, get_task_service

router = APIRouter(prefix="/tasks", tags=["tasks"])


def _not_found(error: TaskNotFoundError) -> HTTPException:
    """Mengubah TaskNotFoundError menjadi respons HTTP 404."""
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))


@router.post("", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(data: TaskCreate, service: TaskService = Depends(get_task_service)) -> Task:
    """Membuat tugas baru."""
    return service.create_task(data)


@router.get("", response_model=list[Task])
def list_tasks(service: TaskService = Depends(get_task_service)) -> list[Task]:
    """Melihat semua tugas."""
    return service.list_tasks()


@router.get("/{task_id}", response_model=Task)
def get_task(task_id: int, service: TaskService = Depends(get_task_service)) -> Task:
    """Melihat tugas berdasarkan ID."""
    try:
        return service.get_task(task_id)
    except TaskNotFoundError as error:
        raise _not_found(error) from error


@router.patch("/{task_id}/status", response_model=Task)
def update_task_status(
    task_id: int,
    data: TaskStatusUpdate,
    service: TaskService = Depends(get_task_service),
) -> Task:
    """Memperbarui status tugas."""
    try:
        return service.update_status(task_id, data.status)
    except TaskNotFoundError as error:
        raise _not_found(error) from error


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, service: TaskService = Depends(get_task_service)) -> Response:
    """Menghapus tugas."""
    try:
        service.delete_task(task_id)
    except TaskNotFoundError as error:
        raise _not_found(error) from error
    return Response(status_code=status.HTTP_204_NO_CONTENT)
