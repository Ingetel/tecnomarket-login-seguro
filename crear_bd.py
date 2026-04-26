import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect("usuarios.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    correo TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    intentos INTEGER DEFAULT 0,
    bloqueado_hasta INTEGER DEFAULT 0
)
""")

clave = generate_password_hash("12345678")

cur.execute("""
INSERT INTO usuarios (correo, password_hash)
VALUES (?, ?)
""", ("admin@tecnomarket.com", clave))

conn.commit()
conn.close()

print("BD creada correctamente")