import sqlite3
from werkzeug.security import generate_password_hash

correo = input("Correo: ").strip().lower()
clave = input("Contraseña: ").strip()

hash_seguro = generate_password_hash(clave)

conn = sqlite3.connect("usuarios.db", timeout=10)
cur = conn.cursor()

try:
    cur.execute(
        "INSERT INTO usuarios (correo, password_hash) VALUES (?, ?)",
        (correo, hash_seguro)
    )
    conn.commit()
    print("Usuario creado correctamente.")

except sqlite3.IntegrityError:
    print("Ese usuario ya existe.")

finally:
    conn.close()