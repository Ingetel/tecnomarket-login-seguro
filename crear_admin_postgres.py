import os
import psycopg2
from werkzeug.security import generate_password_hash

DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("No se encontró DATABASE_URL.")

usuarios = [
    {
        "correo": os.environ.get("ADMIN_CORREO"),
        "password": os.environ.get("ADMIN_PASSWORD")
    },
    {
        "correo": os.environ.get("USUARIO1_CORREO"),
        "password": os.environ.get("USUARIO1_PASSWORD")
    },
    {
        "correo": os.environ.get("USUARIO2_CORREO"),
        "password": os.environ.get("USUARIO2_PASSWORD")
    }
]

conn = psycopg2.connect(DATABASE_URL, sslmode="require")
cur = conn.cursor()

for usuario in usuarios:
    correo = usuario["correo"]
    password = usuario["password"]

    if not correo or not password:
        continue

    correo = correo.strip().lower()
    password_hash = generate_password_hash(password.strip())

    cur.execute("""
        INSERT INTO usuarios (correo, password_hash, intentos, bloqueado_hasta)
        VALUES (%s, %s, 0, 0)
        ON CONFLICT (correo)
        DO UPDATE SET
            password_hash = EXCLUDED.password_hash,
            intentos = 0,
            bloqueado_hasta = 0
    """, (correo, password_hash))

    print(f"Usuario creado o actualizado: {correo}")

conn.commit()
cur.close()
conn.close()

print("Proceso finalizado.")