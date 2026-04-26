import os
import psycopg2
from werkzeug.security import generate_password_hash

DATABASE_URL = os.environ.get("DATABASE_URL")
ADMIN_CORREO = os.environ.get("ADMIN_CORREO", "admin@tecnomarket.com")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "Admin123456")

if not DATABASE_URL:
    raise RuntimeError("No se encontró DATABASE_URL.")

correo = ADMIN_CORREO.strip().lower()
hash_seguro = generate_password_hash(ADMIN_PASSWORD)

conn = psycopg2.connect(DATABASE_URL, sslmode="require")
cur = conn.cursor()

cur.execute("""
    INSERT INTO usuarios (correo, password_hash, intentos, bloqueado_hasta)
    VALUES (%s, %s, 0, 0)
    ON CONFLICT (correo)
    DO UPDATE SET
        password_hash = EXCLUDED.password_hash,
        intentos = 0,
        bloqueado_hasta = 0
""", (correo, hash_seguro))

conn.commit()
cur.close()
conn.close()

print("Usuario administrador creado o actualizado correctamente.")