import os
import psycopg2

DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("No se encontró DATABASE_URL.")

conn = psycopg2.connect(DATABASE_URL, sslmode="require")
cur = conn.cursor()

cur.execute("""
    SELECT id, correo, intentos, bloqueado_hasta
    FROM usuarios
    ORDER BY id
""")

usuarios = cur.fetchall()

if not usuarios:
    print("No hay usuarios registrados.")
else:
    for usuario in usuarios:
        print("ID:", usuario[0])
        print("Correo:", usuario[1])
        print("Intentos:", usuario[2])
        print("Bloqueado hasta:", usuario[3])
        print("-" * 40)

cur.close()
conn.close()