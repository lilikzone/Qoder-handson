# Hands-on Lab: Workshop Qoder AI 60 Menit

Tema: Rules, Context, Agent, MCP, Debugging, dan Testing
Studi kasus: **Task Management API** (Python FastAPI, penyimpanan memori)

| Folder | Fungsi |
|--------|--------|
| `task-management-starter/` | Workspace awal peserta (hanya `app/main.py` + `requirements.txt`) |
| `task-management/` | Solusi referensi & backup bila generasi kode melambat |
| `bahan-workshop/rules/` | Teks Rule A, B, C siap salin |

Skema data tugas:

| Atribut | Tipe | Aturan |
|---------|------|--------|
| `id` | int | otomatis, mulai dari 1 |
| `judul` | str | wajib, 1–100 karakter |
| `deskripsi` | str / null | opsional, maks. 500 karakter |
| `status` | enum | `belum_mulai` (bawaan), `proses`, `selesai` |
| `waktu_dibuat` | datetime | otomatis (UTC) |

Endpoint target: `POST /tasks`, `GET /tasks`, `GET /tasks/{id}`, `PATCH /tasks/{id}/status`, `DELETE /tasks/{id}`

Struktur target:
```
app/main.py
app/models/task.py
app/routes/tasks.py
app/services/task_service.py
tests/test_tasks.py
requirements.txt
README.md
```

> Setiap prompt: salin ke Qoder, periksa rencana dan diff, baru terima perubahan.

---

## Persiapan (sebelum acara)

1. Pasang dan login Qoder IDE; cek menu Rules, Agent, dan MCP tersedia di versi yang dipakai.
2. Pastikan Python 3.11+ terpasang: `python3 --version`.
3. Buka folder `task-management-starter/` di Qoder (**File → Open Folder**).
4. Di terminal Qoder:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
5. Fasilitator: siapkan satu konfigurasi MCP yang sudah berfungsi dan salinan folder `task-management/` sebagai backup.
6. Jangan gunakan kredensial produksi atau data rahasia.

## 00–05 · Orientasi Qoder

1. Tunjukkan panel chat, explorer berkas, terminal, dan tampilan diff.
2. Jelaskan perbedaan mode **Ask** (analisis, tidak mengubah berkas) dan **Agent** (membuat/mengubah berkas).

## 05–12 · Lab 1 — Chat dan Konteks Proyek

1. Pilih mode **Ask**.
2. Kirim **Prompt 1**:
   ```
   Analisis proyek yang sedang terbuka. Jelaskan dengan bahasa Indonesia sederhana:
   1. Bahasa pemrograman dan framework yang digunakan.
   2. Struktur folder dan fungsi tiap folder utama.
   3. Berkas yang menjadi titik awal aplikasi.
   4. Endpoint API yang sudah tersedia.
   5. Dependensi dan cara menjalankan proyek.
   Jangan mengubah berkas apa pun. Jika informasi tidak tersedia, katakan secara jelas.
   ```
3. Verifikasi: Qoder menyebut FastAPI, `app/main.py`, satu endpoint `GET /`, dan tidak ada berkas yang berubah.

## 12–25 · Lab 2 — Rules (materi utama)

1. Buka **Qoder IDE Settings** (`⌘ ⇧ ,` / `Ctrl Shift ,`) → **Rules** → **Add**.
2. Buat **Rule A** — nama `standar-proyek`, tipe **Always Apply**, isi dari `bahan-workshop/rules/rule-a-standar-proyek.md`:
   ```
   Anda adalah pengembang backend Python yang teliti. Untuk proyek ini, ikuti aturan berikut:
   1. Gunakan Python 3.11 atau lebih baru dan FastAPI.
   2. Ikuti PEP 8 dan gunakan anotasi tipe pada fungsi.
   3. Validasi input menggunakan Pydantic.
   4. Pisahkan kode ke routes, services, dan models.
   5. Jangan menulis kata sandi, token, atau kunci API langsung di kode.
   6. Gunakan variabel lingkungan untuk informasi rahasia.
   7. Tambahkan penanganan kesalahan yang sesuai.
   8. Gunakan pytest untuk pengujian logika penting.
   9. Jangan menambah dependensi tanpa menjelaskan alasannya.
   10. Sebelum mengubah kode, jelaskan rencana singkat. Sesudahnya, rangkum berkas yang berubah.
   Selalu jelaskan hasil kepada saya dalam bahasa Indonesia.
   ```
3. Buat **Rule B** — nama `standar-python`, tipe **Specific Files**, pola `**/*.py`, isi dari `rule-b-standar-python.md`:
   ```
   Untuk setiap berkas Python yang dikerjakan:
   - Gunakan snake_case untuk fungsi dan variabel.
   - Gunakan PascalCase untuk nama kelas.
   - Tambahkan anotasi tipe.
   - Buat fungsi yang fokus pada satu tanggung jawab.
   - Gunakan logging untuk diagnostik aplikasi, bukan print.
   - Hindari except tanpa jenis exception.
   - Tambahkan docstring untuk fungsi publik.
   - Jangan mengubah bagian kode yang tidak terkait dengan tugas.
   ```
4. Buat **Rule C** — nama `security-review`, tipe **Apply Manually**, isi dari `rule-c-security-review.md`:
   ```
   Bertindaklah sebagai pemeriksa keamanan aplikasi. Periksa kode yang saya tunjuk untuk:
   1. Kredensial yang ditulis langsung di kode.
   2. Risiko SQL injection.
   3. Validasi input yang tidak memadai.
   4. Penanganan error yang membocorkan informasi.
   5. Pemeriksaan autentikasi dan otorisasi yang kurang.
   6. Paparan data sensitif.
   Kelompokkan temuan berdasarkan tingkat risiko: Kritis, Tinggi, Sedang, Rendah. Berikan bukti dan saran perbaikan. Jangan mengubah berkas sebelum saya menyetujui.
   ```
5. Pastikan berkas Rules muncul di folder `.qoder/rules/`.
6. Pilih mode **Agent**, kirim **Prompt 2**:
   ```
   Buat fungsi untuk mendaftarkan pengguna baru dengan validasi email dan panjang kata sandi serta respons JSON yang terstruktur. Ikuti semua Rules yang berlaku. Sebelum menulis kode, sebutkan standar proyek yang akan Anda terapkan. Setelah selesai, jelaskan bagaimana hasilnya mematuhi Rules.
   ```
7. Diskusi: tunjukkan anotasi tipe, validasi Pydantic, penamaan konsisten, dan tidak ada secret di kode.
8. Tolak/rollback perubahan Prompt 2 agar workspace bersih untuk Lab 3.

## 25–35 · Lab 3 — Agent: Membangun Task Management API

1. Mode **Agent**, kirim **Prompt 3**:
   ```
   Buat REST API manajemen tugas sederhana menggunakan Python FastAPI.
   Fitur: membuat tugas, melihat semua tugas, melihat tugas berdasarkan ID, memperbarui status, dan menghapus tugas.
   Atribut tugas: id, judul, deskripsi, status, waktu_dibuat.
   Persyaratan:
   1. Ikuti semua Rules proyek.
   2. Gunakan Pydantic dan penyimpanan sementara di memori.
   3. Pisahkan routes, services, dan models.
   4. Buat requirements.txt, README.md, dan pengujian pytest.
   5. Jelaskan rencana implementasi sebelum bekerja.
   6. Setelah selesai, jalankan pengujian jika lingkungan memungkinkan.
   7. Laporkan berkas yang dibuat, hasil pengujian yang benar-benar dijalankan, dan kendala yang ditemukan.
   ```
2. Periksa rencana, daftar berkas, dan diff; cocokkan dengan struktur target.
3. Setujui perintah terminal hanya setelah dicek (mis. `pip install`, `pytest`).
4. Jalankan server: `uvicorn app.main:app --reload`.
5. Buka `http://127.0.0.1:8000/docs`, coba kelima endpoint lewat Swagger UI.
6. Bila macet: salin isi folder `task-management/` ke workspace.

## 35–43 · Lab 4 — Referensi Konteks dan MCP

1. Di chat, lampirkan `app/services/task_service.py` dan folder `app/routes/` lewat **@Mention** / tombol konteks (pilih dari antarmuka, bukan diketik).
2. Kirim **Prompt 4**:
   ```
   Gunakan berkas layanan tugas dan folder routes yang saya lampirkan sebagai konteks.
   Periksa:
   1. Logika yang berulang.
   2. Penanganan kesalahan yang kurang.
   3. Pelanggaran terhadap Rules proyek.
   4. Peluang penyederhanaan kode.
   Berikan daftar usulan perbaikan beserta berkas terdampak. Jangan mengubah kode sebelum saya memberikan persetujuan.
   ```
3. Panggil Rule C: ketik `@rule security-review`, lampirkan folder `app/`, minta audit.
4. Fasilitator demo **MCP**: buka konfigurasi MCP yang sudah disiapkan, tunjukkan tool yang tersedia, jelaskan izin akses dan batasannya. Tidak memasang server dari nol.

## 43–53 · Lab 5 — Unit Test dan Debugging

1. Mode **Agent**, kirim **Prompt 5**:
   ```
   Analisis Task Management API yang sudah dibuat. Buat pengujian pytest untuk:
   1. Pembuatan tugas berhasil.
   2. Judul tugas tidak valid.
   3. Tugas tidak ditemukan (HTTP 404).
   4. Pembaruan status tugas.
   5. Penghapusan tugas.
   6. Penanganan input tidak valid.
   Ikuti Rules proyek. Jalankan pengujian bila memungkinkan dan laporkan jumlah yang lulus/gagal, penyebab kegagalan, serta rekomendasi perbaikan. Jangan menyatakan test lulus bila belum dijalankan.
   ```
2. Jalankan sendiri: `pytest -v`, bandingkan dengan laporan Agent.
3. Simulasi bug (opsional): di `task_service.py` ubah `self._next_id += 1` menjadi `self._next_id += 2`, jalankan `pytest` lagi.
4. Kirim **Prompt 6**:
   ```
   Periksa hasil pengujian yang gagal atau error aplikasi. Untuk setiap masalah:
   1. Identifikasi akar penyebabnya.
   2. Jelaskan dampaknya dengan bahasa sederhana.
   3. Usulkan perbaikan terkecil yang aman.
   4. Terapkan perbaikan pada berkas terkait saja.
   5. Jalankan kembali pengujian yang terdampak.
   Tampilkan ringkasan hasil pengujian yang benar-benar dijalankan dan perubahan kode yang dilakukan.
   ```
5. Verifikasi: `pytest -v` kembali hijau.

## 53–60 · Tantangan Akhir dan Q&A

1. Kirim **Prompt 7**:
   ```
   Kembangkan Task Management API dengan menambahkan atribut prioritas dengan pilihan rendah, sedang, dan tinggi. Nilai bawaan adalah sedang. Tolak nilai yang tidak valid dan sediakan filter daftar tugas berdasarkan prioritas. Ikuti semua Rules yang berlaku. Perbarui pengujian otomatis dan README.md. Sebelum mulai, jelaskan berkas yang terdampak. Setelah selesai, jalankan pengujian dan rangkum hasilnya.
   ```
2. Hasil yang diharapkan:
   - Atribut `prioritas`: `rendah` | `sedang` (bawaan) | `tinggi`
   - `POST /tasks` dengan prioritas lain → HTTP 422
   - `GET /tasks?prioritas=tinggi` hanya mengembalikan tugas prioritas tinggi
3. Jalankan `pytest -v`, cek README ikut diperbarui.
4. Tanya jawab.

---

## Checklist Peserta

- [ ] Dapat menjelaskan perbedaan mode analisis (Ask) dan mode Agent
- [ ] Rule A (Always Apply) dibuat
- [ ] Rule B (Specific Files `**/*.py`) dibuat
- [ ] Rule C (Apply Manually) dipanggil untuk audit keamanan
- [ ] Memberi konteks berkas/folder lewat @Mention
- [ ] Agent membuat Task Management API sesuai struktur target
- [ ] `pytest -v` dijalankan dan hasilnya diperiksa
- [ ] Field `prioritas` ditambahkan (tantangan)

Referensi: https://docs.qoder.com/user-guide/rules · https://docs.qoder.com/user-guide/chat/overview
