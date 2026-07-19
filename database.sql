-- ============================================================
-- database.sql
-- Skema database aplikasi Portofolio (TiDB / kompatibel MySQL)
-- Jalankan sekali di awal, misal:
--   mysql -h <TIDB_HOST> -P 4000 -u <user> -p --ssl-mode=VERIFY_IDENTITY < database.sql
-- atau lewat TiDB Cloud SQL Editor.
-- ============================================================

CREATE DATABASE IF NOT EXISTS portofolio_db;
USE portofolio_db;

-- ---------------- users ----------------
-- Akun admin yang bisa login ke panel admin.
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'admin',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ---------------- profiles ----------------
-- Data profil pemilik portofolio (satu baris per user_id).
CREATE TABLE IF NOT EXISTS profiles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    nama_lengkap VARCHAR(150) NOT NULL DEFAULT '',
    nama_panggilan VARCHAR(80),
    tempat_lahir VARCHAR(100),
    tanggal_lahir DATE NULL,
    email VARCHAR(150),
    telepon VARCHAR(30),
    universitas VARCHAR(150),
    fakultas VARCHAR(150),
    prodi VARCHAR(150),
    semester VARCHAR(10),
    alamat VARCHAR(255),
    foto_url VARCHAR(500),
    foto_public_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ---------------- skills ----------------
CREATE TABLE IF NOT EXISTS skills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    nama_skill VARCHAR(100) NOT NULL,
    icon_class VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ---------------- experiences ----------------
CREATE TABLE IF NOT EXISTS experiences (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    posisi VARCHAR(150) NOT NULL,
    perusahaan VARCHAR(150) NOT NULL,
    durasi VARCHAR(100),
    deskripsi TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ---------------- projects ----------------
CREATE TABLE IF NOT EXISTS projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    judul VARCHAR(150) NOT NULL,
    deskripsi TEXT,
    gambar_url VARCHAR(500),
    gambar_public_id VARCHAR(255),
    link_project VARCHAR(300),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ---------------- contacts ----------------
-- Pesan yang dikirim pengunjung lewat form kontak di halaman utama.
CREATE TABLE IF NOT EXISTS contacts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL,
    message TEXT NOT NULL,
    is_read TINYINT(1) NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
