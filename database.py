import sqlite3
from random import randint

conn = sqlite3.connect("inventaris.db")
cursor = conn.cursor()

# 0 - User
# 1 - Admin

cursor.executescript("""
CREATE TABLE IF NOT EXISTS user(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(255),
    password VARCHAR(255),
    status TINYINT
);

CREATE TABLE IF NOT EXISTS barang(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_barang VARCHAR(50),
    jumlah INTEGER,
    kondisi VARCHAR(50),
    lokasi VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS kondisi(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teks VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS lokasi(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teks VARCHAR(50)
)
""")


cursor.execute("SELECT * FROM user")
print(cursor.fetchall())

conn.commit()
conn.close()
print("Database berhasil dibuat!")