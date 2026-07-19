"""
model.py
--------
Wrapper koneksi database ke TiDB (protokol MySQL) menggunakan PyMySQL.
Dipakai oleh seluruh blueprint di Backend/admin dan Backend/utama lewat:

    from model import Database
    db = Database()
    db.execute_query(query, params, fetch=True/False)

Setiap pemanggilan membuka koneksi baru dan menutupnya lagi setelah query
selesai -- cukup untuk skala tugas/portofolio ini dan aman dari koneksi
menggantung ("stale connection") pada TiDB Cloud Serverless.
"""

import certifi
import pymysql
from pymysql.cursors import DictCursor

from config import Config


class Database:
    def get_connection(self):
        ssl_args = None
        if Config.DB_SSL_ENABLED:
            ssl_args = {"ca": Config.DB_SSL_CA or certifi.where()}

        return pymysql.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME,
            cursorclass=DictCursor,
            ssl=ssl_args,
            autocommit=True,
            connect_timeout=10,
        )

    def execute_query(self, query, params=None, fetch=False):
        """Jalankan satu query SQL.

        - fetch=True  -> mengembalikan list of dict hasil SELECT.
        - fetch=False -> untuk INSERT mengembalikan lastrowid (id baru),
                          untuk UPDATE/DELETE mengembalikan jumlah baris terdampak.
        """
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params or ())

                if fetch:
                    return cursor.fetchall()

                statement = query.strip().split(None, 1)[0].upper()
                if statement == "INSERT":
                    return cursor.lastrowid
                return cursor.rowcount
        finally:
            conn.close()
