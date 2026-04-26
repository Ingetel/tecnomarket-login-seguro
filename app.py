from flask import Flask, render_template, request, redirect, session
import sqlite3
import time
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "tecnomarket_secret_key"

DB = os.path.join(os.path.dirname(__file__), "usuarios.db")
MAX_INTENTOS = 3
BLOQUEO_SEG = 60


def get_db():
    return sqlite3.connect(DB)


def buscar_usuario(correo):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, correo, password_hash, intentos, bloqueado_hasta
        FROM usuarios
        WHERE correo = ?
    """, (correo,))

    row = cur.fetchone()
    conn.close()
    return row


def actualizar_intentos(user_id, intentos, bloqueo):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        UPDATE usuarios
        SET intentos=?, bloqueado_hasta=?
        WHERE id=?
    """, (intentos, bloqueo, user_id))

    conn.commit()
    conn.close()


@app.route("/")
def index():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():

    correo = request.form.get("correo", "").strip().lower()
    password = request.form.get("password", "").strip()

    if not correo or not password:
        return "Credenciales inválidas"

    user = buscar_usuario(correo)

    if not user:
        time.sleep(1)
        return "Credenciales inválidas"

    user_id, _, pass_hash, intentos, bloqueado_hasta = user
    ahora = int(time.time())

    if bloqueado_hasta and ahora < bloqueado_hasta:
        return "Cuenta bloqueada temporalmente"

    if check_password_hash(pass_hash, password):

        actualizar_intentos(user_id, 0, 0)
        session["usuario"] = correo
        return redirect("/panel")

    else:
        intentos += 1
        bloqueo = 0

        if intentos >= MAX_INTENTOS:
            bloqueo = ahora + BLOQUEO_SEG
            intentos = 0

        actualizar_intentos(user_id, intentos, bloqueo)

        time.sleep(1)
        return "Credenciales inválidas"


@app.route("/panel")
def panel():
    if "usuario" not in session:
        return redirect("/")
    return """
<!DOCTYPE html>
<html lang='es'>
<head>
<title>Panel</title>
<style>
body{
background:#061006;
color:white;
font-family:Arial;
display:flex;
justify-content:center;
align-items:center;
height:100vh;
margin:0;
}
.box{
background:#111;
padding:40px;
border-radius:15px;
box-shadow:0 0 30px rgba(0,255,65,.2);
text-align:center;
}
h1{color:#00ff41;}
a{
display:inline-block;
margin-top:20px;
padding:10px 20px;
background:#00ff41;
color:black;
text-decoration:none;
font-weight:bold;
border-radius:8px;
}
</style>
</head>
<body>
<div class='box'>
<h1>Bienvenido a TecnoMarket</h1>
<p>Acceso autorizado</p>
<a href='/'>Cerrar sesión</a>
</div>
</body>
</html>
"""


if __name__ == "__main__":
    app.run(debug=True)