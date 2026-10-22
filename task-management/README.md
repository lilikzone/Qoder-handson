# Task Management API (Solusi Referensi)

REST API manajemen tugas dengan Python FastAPI untuk Workshop Qoder AI 60 Menit.
Penyimpanan sementara di memori (data hilang saat server restart).
Folder ini juga dipakai sebagai **backup proyek** bila generasi kode saat workshop melambat.

## Menjalankan

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload     # http://127.0.0.1:8000/docs
pytest -v
```

## Struktur

```
app/main.py                    # titik awal aplikasi
app/models/task.py             # model Pydantic
app/routes/tasks.py            # endpoint /tasks
app/services/task_service.py   # logika bisnis + penyimpanan memori
tests/test_tasks.py            # pengujian pytest
```

## Endpoint

| Method | Endpoint             | Keterangan              |
|--------|----------------------|-------------------------|
| POST   | /tasks               | Membuat tugas           |
| GET    | /tasks               | Melihat semua tugas     |
| GET    | /tasks/{id}          | Melihat tugas per ID    |
| PATCH  | /tasks/{id}/status   | Memperbarui status      |
| DELETE | /tasks/{id}          | Menghapus tugas         |

Atribut tugas: `id`, `judul`, `deskripsi`, `status` (`belum_mulai` | `proses` | `selesai`), `waktu_dibuat`.

> Catatan: API ini tanpa autentikasi, hanya untuk demo lokal.
