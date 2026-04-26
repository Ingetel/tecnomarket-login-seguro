import sqlite3

DB_NAME = "usuarios.db"

conn = sqlite3.connect(DB_NAME)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    correo TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    intentos INTEGER DEFAULT 0,
    bloqueado_hasta INTEGER DEFAULT 0
)
""")

conn.commit()
conn.close()

print("BD creada correctamente.")
