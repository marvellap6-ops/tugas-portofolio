from flask import Blueprint, jsonify

from model import Database
from Backend.admin.login import token_required

contacts_bp = Blueprint("contacts", __name__)


@contacts_bp.route("/contacts", methods=["GET"])
@token_required
def get_contacts(current_user):
    """Mengambil seluruh pesan kontak (Admin Only)."""
    try:
        db = Database()
        query = "SELECT * FROM contacts ORDER BY created_at DESC"
        result = db.execute_query(query, fetch=True)

        return jsonify({"success": True, "data": result if result else []}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@contacts_bp.route("/contacts/<int:id>/read", methods=["PUT"])
@token_required
def mark_contact_read(current_user, id):
    """Menandai satu pesan kontak sebagai sudah dibaca (Admin Only)."""
    try:
        db = Database()
        db.execute_query("UPDATE contacts SET is_read = 1 WHERE id = %s", (id,))
        return jsonify({"success": True, "message": "Pesan ditandai sudah dibaca"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@contacts_bp.route("/contacts/<int:id>", methods=["DELETE"])
@token_required
def delete_contact(current_user, id):
    """Menghapus satu pesan kontak (Admin Only)."""
    try:
        db = Database()
        db.execute_query("DELETE FROM contacts WHERE id = %s", (id,))
        return jsonify({"success": True, "message": "Pesan berhasil dihapus"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
