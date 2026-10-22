"""Pengujian Task Management API."""

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.task_service import TaskService, get_task_service


@pytest.fixture
def client() -> Iterator[TestClient]:
    """Client dengan penyimpanan baru untuk setiap test."""
    service = TaskService()
    app.dependency_overrides[get_task_service] = lambda: service
    yield TestClient(app)
    app.dependency_overrides.clear()


def _buat_tugas(client: TestClient, judul: str = "Belajar Qoder") -> dict:
    response = client.post("/tasks", json={"judul": judul, "deskripsi": "Ikuti workshop"})
    assert response.status_code == 201
    return response.json()


def test_buat_tugas_berhasil(client: TestClient) -> None:
    tugas = _buat_tugas(client)
    assert tugas["id"] == 1
    assert tugas["judul"] == "Belajar Qoder"
    assert tugas["status"] == "belum_mulai"
    assert "waktu_dibuat" in tugas


@pytest.mark.parametrize("judul", ["", "   ", "x" * 101])
def test_judul_tidak_valid(client: TestClient, judul: str) -> None:
    response = client.post("/tasks", json={"judul": judul})
    assert response.status_code == 422


def test_lihat_semua_dan_per_id(client: TestClient) -> None:
    _buat_tugas(client, "Tugas 1")
    _buat_tugas(client, "Tugas 2")
    assert len(client.get("/tasks").json()) == 2
    assert client.get("/tasks/2").json()["judul"] == "Tugas 2"


def test_tugas_tidak_ditemukan(client: TestClient) -> None:
    response = client.get("/tasks/999")
    assert response.status_code == 404
    assert "tidak ditemukan" in response.json()["detail"]


def test_perbarui_status(client: TestClient) -> None:
    tugas = _buat_tugas(client)
    response = client.patch(f"/tasks/{tugas['id']}/status", json={"status": "selesai"})
    assert response.status_code == 200
    assert response.json()["status"] == "selesai"


def test_hapus_tugas(client: TestClient) -> None:
    tugas = _buat_tugas(client)
    assert client.delete(f"/tasks/{tugas['id']}").status_code == 204
    assert client.get(f"/tasks/{tugas['id']}").status_code == 404
    assert client.delete(f"/tasks/{tugas['id']}").status_code == 404


@pytest.mark.parametrize(
    "payload",
    [{}, {"judul": 123}, {"judul": "ok", "deskripsi": "x" * 501}],
)
def test_input_buat_tidak_valid(client: TestClient, payload: dict) -> None:
    assert client.post("/tasks", json=payload).status_code == 422


def test_status_tidak_valid(client: TestClient) -> None:
    tugas = _buat_tugas(client)
    response = client.patch(f"/tasks/{tugas['id']}/status", json={"status": "batal"})
    assert response.status_code == 422
