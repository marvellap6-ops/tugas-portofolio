"""
Backend/utama/utama.py
-----------------------
Blueprint publik (tanpa login) untuk halaman utama portofolio.

Endpoint:
- GET  /api/main-profile  -> profil + skills + experiences + projects (untuk index.html)
- POST /api/contact       -> simpan pesan kontak ke DB + kirim notifikasi via Resend
"""

import resend
from flask import Blueprint, jsonify, request

from config import Config
from model import Database

utama_bp = Blueprint("utama", __name__)

resend.api_key = Config.RESEND_API_KEY


@utama_bp.route("/main-profile", methods=["GET"])
def main_profile():
    """Mengambil seluruh data publik (profil, skill, pengalaman, proyek)
    milik admin, untuk ditampilkan secara dinamis di index.html."""
    try:
        db = Database()

        query_profile = """
            SELECT p.*
            FROM profiles p
            JOIN users u ON p.user_id = u.id
            WHERE u.role = 'admin'
            ORDER BY p.id ASC
            LIMIT 1
        """
        profile_result = db.execute_query(query_profile, fetch=True)

        if not profile_result:
            return jsonify({"success": False, "error": "Profil belum diisi oleh admin"}), 404

        profile = profile_result[0]
        user_id = profile["user_id"]

        skills = db.execute_query(
            "SELECT * FROM skills WHERE user_id = %s ORDER BY id ASC",
            (user_id,),
            fetch=True,
        ) or []

        experiences = db.execute_query(
            "SELECT * FROM experiences WHERE user_id = %s ORDER BY created_at DESC",
            (user_id,),
            fetch=True,
        ) or []

        projects = db.execute_query(
            "SELECT * FROM projects WHERE user_id = %s ORDER BY created_at DESC",
            (user_id,),
            fetch=True,
        ) or []

        data = dict(profile)
        data["skills"] = skills
        data["experiences"] = experiences
        data["projects"] = projects

        return jsonify({"success": True, "data": data}), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@utama_bp.route("/contact", methods=["POST"])
def contact():
    """Menerima pesan dari form kontak pengunjung, simpan ke DB,
    lalu kirim notifikasi email ke pemilik portofolio via Resend."""
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "Request body harus JSON"}), 400

        name = (data.get("name") or "").strip()
        email = (data.get("email") or "").strip()
        message = (data.get("message") or "").strip()

        if not name or not email or not message:
            return jsonify({"error": "Nama, email, dan pesan wajib diisi"}), 400

        db = Database()
        db.execute_query(
            "INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)",
            (name, email, message),
        )

        _send_contact_email(name, email, message)

        return jsonify({"success": True, "message": "Pesan berhasil dikirim. Terima kasih!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def _send_contact_email(name, email, message):
    """Kirim notifikasi via Resend. Kegagalan kirim email TIDAK menggagalkan
    penyimpanan pesan kontak (pesan tetap tersimpan di database)."""
    receiver = Config.CONTACT_RECEIVER_EMAIL

    if not receiver or not Config.RESEND_API_KEY:
        print("[RESEND WARNING] CONTACT_RECEIVER_EMAIL / RESEND_API_KEY belum diisi di .env; "
              "email tidak dikirim.")
        return

    try:
        resend.Emails.send(
            {
                "from": Config.RESEND_FROM_EMAIL,
                "to": [receiver],
                "reply_to": email,
                "subject": f"[Portfolio] Pesan baru dari {name}",
                "html": f"""
                    <div style="font-family: Arial, sans-serif; max-width: 600px;">
                        <h2>Pesan Baru dari Formulir Kontak</h2>
                        <p><strong>Nama:</strong> {name}</p>
                        <p><strong>Email:</strong> {email}</p>
                        <p><strong>Pesan:</strong></p>
                        <p style="white-space: pre-wrap; background:#f5f5f5; padding:12px; border-radius:8px;">
                            {message}
                        </p>
                    </div>
                """,
            }
        )
    except Exception as e:
        print(f"[RESEND WARNING] Gagal mengirim email: {e}")
