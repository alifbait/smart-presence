# Smart Presence - Sistem Presensi Pegawai Berbasis Web

Smart Presence adalah sistem presensi pegawai berbasis web yang dibuat menggunakan Django Framework.
Sistem ini mendukung autentikasi pengguna, role management, presensi harian, pengajuan izin, dashboard statistik, dan simulasi hari libur nasional menggunakan API internal sederhana.

---

# Fitur Utama

## Autentikasi Pengguna

* Login & Logout
* Role pengguna:

  * Superuser
  * Admin
  * Pegawai

## Dashboard Presensi

* Statistik kehadiran
* Statistik keterlambatan
* Statistik izin/sakit
* Tampilan modern responsive

## Presensi Harian

* Presensi masuk
* Presensi pulang
* Status kehadiran otomatis:

  * Hadir
  * Terlambat
  * Izin
  * Alpa

## Pengajuan Izin

* Izin
* Sakit
* Cuti
* Upload bukti file

## Sistem Hari Libur Nasional

* API internal sederhana
* Simulasi hari libur nasional
* Presensi otomatis dinonaktifkan saat hari libur

## Django Admin

* Kelola pegawai
* Kelola presensi
* Kelola pengajuan izin

---

# Teknologi yang Digunakan

* Python 3.14
* Django 5
* Bootstrap 5
* SQLite3
* HTML5
* CSS3
* JavaScript

---

# Struktur Role Pengguna

| Role      | Hak Akses                             |
| --------- | ------------------------------------- |
| Superuser | Akses penuh Django Admin              |
| Admin     | Kelola data pegawai & presensi        |
| Pegawai   | Melakukan presensi dan pengajuan izin |

---

# Cara Menjalankan Project

## 1. Clone Repository

```bash
git clone https://github.com/USERNAME/smart-presence.git
cd smart-presence
```

---

## 2. Buat Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / MacOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependency

```bash
pip install -r requirements.txt
```

---

## 4. Jalankan Migration

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 5. Buat Superuser

```bash
python manage.py createsuperuser
```

Isi username, email, dan password sesuai kebutuhan.

---

## 6. Jalankan Server

```bash
python manage.py runserver
```

Buka browser:

```text
http://127.0.0.1:8000/
```

---

# Akses Admin Django

```text
http://127.0.0.1:8000/admin/
```

Login menggunakan akun superuser.

---

# Endpoint API Hari Libur

```text
/presensi/api/hari-libur/
```

Contoh response:

```json
{
  "tanggal": "2026-06-04",
  "is_holiday": true,
  "holiday_name": "Hari Libur Simulasi Demo",
  "holiday_description": "Sistem presensi dinonaktifkan karena hari libur nasional/simulasi demo.",
  "source": "Internal Holiday Service",
  "test_mode": true
}
```

---

# Catatan Pengembangan

Project ini dibuat untuk pembelajaran dan pengembangan sistem presensi modern berbasis web menggunakan Django Framework.

---

# Developer

Developed by:

*Alif Baiatur Ridhwan El Habibie

---

# License

Project ini digunakan untuk kebutuhan pembelajaran dan pengembangan akademik.
