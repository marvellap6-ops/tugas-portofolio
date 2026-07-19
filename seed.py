"""
seed.py
-------
Jalankan skrip ini SEKALI setelah `database.sql` dieksekusi, untuk membuat
akun admin pertama dengan password yang sudah di-hash (bukan ditulis manual
di SQL) dan baris profil kosong sebagai titik awal.

Cara pakai:
    python seed.py

Username & password diambil dari .env (ADMIN_USERNAME, ADMIN_PASSWORD).
"""

from werkzeug.security import generate_password_hash

from config import Config
from model import Database


def main():
    db = Database()

    existing = db.execute_query(
        "SELECT id FROM users WHERE username = %s", (Config.ADMIN_USERNAME,), fetch=True
    )

    if existing:
        print(f"User '{Config.ADMIN_USERNAME}' sudah ada, skip pembuatan user.")
        user_id = existing[0]["id"]
    else:
        password_hash = generate_password_hash(Config.ADMIN_PASSWORD)
        user_id = db.execute_query(
            "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, 'admin')",
            (Config.ADMIN_USERNAME, password_hash),
        )
        print(f"User admin '{Config.ADMIN_USERNAME}' berhasil dibuat (id={user_id}).")

    profile_exists = db.execute_query(
        "SELECT id FROM profiles WHERE user_id = %s", (user_id,), fetch=True
    )

    if profile_exists:
        print("Baris profil untuk admin ini sudah ada, skip.")
    else:
        db.execute_query(
            "INSERT INTO profiles (user_id, nama_lengkap) VALUES (%s, %s)",
            (user_id, "Nama Anda"),
        )
        print("Baris profil kosong berhasil dibuat -- lengkapi lewat halaman admin.")

    print("\nSelesai. Login ke /admin dengan:")
    print(f"  username: {Config.ADMIN_USERNAME}")
    print(f"  password: (sesuai ADMIN_PASSWORD di .env)")


if __name__ == "__main__":
    main()
