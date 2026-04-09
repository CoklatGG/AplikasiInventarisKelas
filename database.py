import sqlite3

conn = sqlite3.connect("siswa.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS user(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(255),
    password VARCHAR(255),
    status TINYINT
)
""")

conn.commit()
conn.close()
print("Database berhasil dibuat!")