import os
import sqlite3
from werkzeug.security import generate_password_hash

DB_NAME = "usuarios.db"

# Render usará estas variables de entorno.
# Si no existen, se usarán estos valores por defecto para prueba académica.
correo = os.environ.get("ADMIN_CORREO", "admin@tecnomarket.com").strip().lower()
clave = os.environ.get("ADMIN_PASSWORD", "Admin123*").strip()

hash_seguro = generate_password_hash(clave)

conn = sqlite3.connect(DB_NAME, timeout=10)
cur = conn.cursor()

try:
    cur.execute(
        """
        INSERT OR IGNORE INTO usuarios (correo, password_hash)
        VALUES (?, ?)
        """,
        (correo, hash_seguro)
    )

    conn.commit()

    if cur.rowcount == 0:
        print("El usuario administrador ya existe.")
    else:
        print("Usuario administrador creado correctamente.")

finally:
    conn.close()
