from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'clave_secreta_cambiala'

# 📦 CREAR BASE DE DATOS AUTOMÁTICAMENTE
def init_db():
    conn = sqlite3.connect("citas.db")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mascota TEXT NOT NULL,
            propietario TEXT NOT NULL,
            especie TEXT,
            fecha TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

# Ejecutar al iniciar
init_db()

# 🔗 FUNCIÓN DE CONEXIÓN
def get_db():
    return sqlite3.connect("citas.db")

# 🏠 AGENDA (VER CITAS)
@app.route('/')
def index():
    conn = get_db()
    citas = conn.execute("SELECT * FROM pacientes").fetchall()
    conn.close()
    return render_template('index.html', citas=citas)

# 🟢 AGENDAR CITA
@app.route('/agendar', methods=['GET', 'POST'])
def agendar():
    if request.method == 'POST':
        mascota = request.form['mascota']
        propietario = request.form['propietario']
        especie = request.form['especie']
        fecha = request.form['fecha']

        try:
            conn = get_db()
            conn.execute("""
                INSERT INTO pacientes (mascota, propietario, especie, fecha)
                VALUES (?, ?, ?, ?)
            """, (mascota, propietario, especie, fecha))

            conn.commit()
            conn.close()

            flash('Cita registrada correctamente', 'success')

        except Exception as e:
            print("Error:", e)
            flash('Error al registrar cita', 'danger')

        return redirect(url_for('index'))

    return render_template('agendar.html')

# 🟡 EDITAR CITA
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    conn = get_db()

    if request.method == 'POST':
        mascota = request.form['mascota']
        propietario = request.form['propietario']
        especie = request.form['especie']
        fecha = request.form['fecha']

        conn.execute("""
            UPDATE pacientes
            SET mascota=?, propietario=?, especie=?, fecha=?
            WHERE id=?
        """, (mascota, propietario, especie, fecha, id))

        conn.commit()
        conn.close()

        flash('Cita actualizada', 'warning')
        return redirect(url_for('index'))

    cita = conn.execute("SELECT * FROM pacientes WHERE id=?", (id,)).fetchone()
    conn.close()

    return render_template('editar.html', cita=cita)

# 🔴 ELIMINAR CITA
@app.route('/eliminar/<int:id>')
def eliminar(id):
    conn = get_db()
    conn.execute("DELETE FROM pacientes WHERE id=?", (id,))
    conn.commit()
    conn.close()

    flash('Cita eliminada', 'danger')
    return redirect(url_for('index'))

# ▶️ EJECUTAR
if __name__ == '__main__':
    app.run(debug=True)