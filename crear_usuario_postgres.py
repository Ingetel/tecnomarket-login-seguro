import os
import getpass
import psycopg2
from werkzeug.security import generate_password_hash

DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("No se encontró DATABASE_URL.")

correo = input("Correo: ").strip().lower()
clave = getpass.getpass("Contraseña: ").strip()

if not correo or not clave:
    print("Correo y contraseña son obligatorios.")
    exit()

hash_seguro = generate_password_hash(clave)

conn = psycopg2.connect(DATABASE_URL, sslmode="require")
cur = conn.cursor()

try:
    cur.execute("""
        INSERT INTO usuarios (correo, password_hash, intentos, bloqueado_hasta)
        VALUES (%s, %s, 0, 0)
    """, (correo, hash_seguro))

    conn.commit()
    print("Usuario creado correctamente.")

except psycopg2.errors.UniqueViolation:
    conn.rollback()
    print("Ese usuario ya existe.")

finally:
    cur.close()
    conn.close()