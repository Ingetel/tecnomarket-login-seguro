from flask import Flask, render_template, request, redirect, session, url_for
import time
import os
import re
import psycopg2
from werkzeug.security import check_password_hash

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY", "tecnomarket_secret_key")

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax"
)

MAX_INTENTOS = 3
BLOQUEO_SEG = 60
CAMPOS_ESPERADOS = {"correo", "password"}


def get_db():
    database_url = os.environ.get("DATABASE_URL")

    if not database_url:
        raise RuntimeError("No se encontró la variable DATABASE_URL.")

    return psycopg2.connect(database_url, sslmode="require")


def validar_entrada(correo, password):
    if not correo or not password:
        return False

    if len(correo) > 100 or len(password) > 100:
        return False

    patron_correo = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    if not re.match(patron_correo, correo):
        return False

    return True


def solicitud_esperada():
    campos_recibidos = set(request.form.keys())
    return campos_recibidos.issubset(CAMPOS_ESPERADOS)


def buscar_usuario(correo):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, correo, password_hash, intentos, bloqueado_hasta
        FROM usuarios
        WHERE correo = %s
    """, (correo,))

    row = cur.fetchone()

    cur.close()
    conn.close()

    return row


def actualizar_intentos(user_id, intentos, bloqueo):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        UPDATE usuarios
        SET intentos = %s,
            bloqueado_hasta = %s
        WHERE id = %s
    """, (intentos, bloqueo, user_id))

    conn.commit()

    cur.close()
    conn.close()


@app.route("/")
def index():
    return render_template("login.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    mensaje_error = "Credenciales inválidas."

    # Si alguien abre /login directamente desde el navegador,
    # se redirige al formulario. El procesamiento real solo ocurre por POST.
    if request.method == "GET":
        return redirect(url_for("index"))

    # Procesa únicamente los campos esperados del formulario.
    if not solicitud_esperada():
        time.sleep(1)
        return render_template("login.html", error=mensaje_error)

    correo = request.form.get("correo", "").strip().lower()
    password = request.form.get("password", "").strip()

    # Validación de entradas.
    if not validar_entrada(correo, password):
        time.sleep(1)
        return render_template("login.html", error=mensaje_error)

    user = buscar_usuario(correo)

    # Mensaje genérico: no revela si el correo existe o no.
    if not user:
        time.sleep(1)
        return render_template("login.html", error=mensaje_error)

    user_id, correo_db, pass_hash, intentos, bloqueado_hasta = user
    ahora = int(time.time())

    # Control contra fuerza bruta: bloqueo temporal.
    # Se mantiene un mensaje genérico para no revelar información sensible.
    if bloqueado_hasta and ahora < bloqueado_hasta:
        time.sleep(1)
        return render_template("login.html", error=mensaje_error)

    # Credenciales correctas.
    if check_password_hash(pass_hash, password):
        actualizar_intentos(user_id, 0, 0)
        session["usuario"] = correo_db
        return redirect(url_for("panel"))

    # Credenciales incorrectas: aumenta contador de intentos.
    intentos += 1
    bloqueo = 0

    if intentos >= MAX_INTENTOS:
        bloqueo = ahora + BLOQUEO_SEG
        intentos = 0

    actualizar_intentos(user_id, intentos, bloqueo)

    time.sleep(1)
    return render_template("login.html", error=mensaje_error)


@app.route("/panel")
def panel():
    if "usuario" not in session:
        return redirect(url_for("index"))

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
<a href='/logout'>Cerrar sesión</a>
</div>
</body>
</html>
"""


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=False)
