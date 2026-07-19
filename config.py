import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Seluruh konfigurasi dibaca dari environment variable (.env) via os.getenv()."""

    # ---------------- Flask ----------------
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-jangan-dipakai-di-production")
    DEBUG = os.getenv("FLASK_DEBUG", "True").strip().lower() == "true"

    # ---------------- TiDB (MySQL protocol via PyMySQL) ----------------
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = int(os.getenv("DB_PORT", "4000"))
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    # TiDB Cloud (serverless) mewajibkan koneksi TLS/SSL.
    DB_SSL_ENABLED = os.getenv("DB_SSL_ENABLED", "True").strip().lower() == "true"
    # Opsional: path ke file CA custom. Jika kosong, pakai bundel CA dari certifi.
    DB_SSL_CA = os.getenv("DB_SSL_CA")

    # ---------------- Cloudinary (penyimpanan gambar) ----------------
    CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

    # ---------------- Resend (pengiriman email) ----------------
    RESEND_API_KEY = os.getenv("RESEND_API_KEY")
    RESEND_FROM_EMAIL = os.getenv("RESEND_FROM_EMAIL", "Portfolio <onboarding@resend.dev>")
    # Email tujuan saat ada pesan kontak baru dari pengunjung.
    CONTACT_RECEIVER_EMAIL = os.getenv("CONTACT_RECEIVER_EMAIL")

    # ---------------- Admin default (dipakai oleh seed.py) ----------------
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

    # ---------------- Upload ----------------
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024  # batas upload 8 MB
