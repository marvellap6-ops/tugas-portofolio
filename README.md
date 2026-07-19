# Portofolio Web — Flask + TiDB + Cloudinary + Resend

Aplikasi web portofolio dengan halaman utama dinamis dan panel admin (CRUD
penuh) untuk Profil, Skill, Pengalaman, Proyek, dan Pesan Kontak.

## Arsitektur

- **Backend**: Flask, koneksi ke **TiDB** (protokol MySQL) lewat PyMySQL raw
  query (kelas `Database` di `model.py`), autentikasi admin dengan **JWT**.
- **Frontend**: HTML + CSS + JavaScript murni (tanpa framework), memanggil
  backend lewat `fetch()`.
- **Cloudinary**: upload gambar (foto profil & gambar proyek).
- **Resend**: kirim email notifikasi saat ada pesan kontak baru dari
  pengunjung.

Seluruh kredensial dibaca dari `.env` lewat `os.getenv()` (lihat `config.py`).

## 1. Setup Layanan

### TiDB Cloud
1. Buat cluster **Serverless** gratis di https://tidbcloud.com
2. Buka tab **Connect**, catat: host, port (4000), username, password.
3. Buat database baru, misalnya `portofolio_db`.

### Cloudinary
1. Daftar di https://cloudinary.com
2. Di Dashboard, catat: Cloud Name, API Key, API Secret.

### Resend
1. Daftar di https://resend.com
2. Buat API Key di menu **API Keys**.
3. Untuk uji coba lokal, kamu bisa memakai alamat pengirim default
   `onboarding@resend.dev` (tidak perlu verifikasi domain).

## 2. Instalasi

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 3. Konfigurasi `.env`

```bash
cp .env.example .env
```

Isi semua nilai di `.env` sesuai kredensial TiDB, Cloudinary, dan Resend
kamu (lihat komentar di masing-masing baris `.env.example`).

## 4. Setup Database

Jalankan skema tabel (lewat SQL client apa pun yang bisa konek ke TiDB,
atau lewat **SQL Editor** di dashboard TiDB Cloud):

```bash
mysql -h <DB_HOST> -P 4000 -u <DB_USER> -p --ssl-mode=VERIFY_IDENTITY < database.sql
```

Lalu buat akun admin pertama (password di-hash otomatis, bukan ditulis
manual di SQL):

```bash
python seed.py
```

Ini akan membuat:
- 1 user admin (username/password sesuai `ADMIN_USERNAME` / `ADMIN_PASSWORD` di `.env`)
- 1 baris profil kosong yang siap dilengkapi lewat panel admin

## 5. Jalankan Aplikasi

```bash
python app.py
```

- Halaman utama: http://localhost:5000
- Panel admin: http://localhost:5000/admin

## Struktur API

| Method | Endpoint | Auth | Keterangan |
|---|---|---|---|
| POST | `/api/login` | - | Login admin, mengembalikan JWT |
| POST | `/api/logout` | - | Logout (hapus session) |
| GET | `/api/auth/check` | JWT | Cek status login |
| GET | `/api/main-profile` | - | Data publik: profil + skill + pengalaman + proyek |
| POST | `/api/contact` | - | Kirim pesan kontak (simpan ke DB + email via Resend) |
| GET/PUT | `/api/profiles` | JWT | Baca/ubah profil |
| GET/POST/PUT/DELETE | `/api/skills[/​<id>]` | GET publik, sisanya JWT | CRUD skill |
| GET/POST/PUT/DELETE | `/api/experiences[/​<id>]` | GET publik, sisanya JWT | CRUD pengalaman |
| GET/POST/PUT/DELETE | `/api/projects[/​<id>]` | GET publik, sisanya JWT | CRUD proyek |
| GET/PUT/DELETE | `/api/contacts[/​<id>]` | JWT | Lihat / tandai dibaca / hapus pesan kontak |
| POST | `/api/upload/image` | JWT | Upload gambar ke Cloudinary, kembalikan URL |
| GET | `/api/dashboard/stats` | JWT | Statistik untuk dashboard admin |
| GET | `/api/dashboard/recent` | JWT | Aktivitas terbaru |

## Catatan Keamanan

1. Password admin di-hash dengan Werkzeug (tidak pernah disimpan plain text).
2. Autentikasi admin memakai JWT dengan masa berlaku 24 jam.
3. `.env` **jangan** pernah di-commit ke Git (sudah ada `.gitignore`).
4. CORS di-enable untuk `/api/*` — batasi origin di production jika perlu.
