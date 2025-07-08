from flask import Flask, render_template, request, redirect, flash, session, url_for
from werkzeug.utils import secure_filename
from datetime import datetime
import sqlite3
import os
import hashlib

app = Flask(__name__)
app.secret_key = 'rahasia'

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

DB_FILE = 'users.db'

# Inisialisasi database
def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS users ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "username TEXT UNIQUE,"
            "password TEXT,"
            "photo TEXT,"
            "created_at TEXT)"
        )

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_user(username):
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        return cur.fetchone()

@app.route('/')
def home():
    if "username" in session:
        return redirect("/profile")
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = get_user(username)
    if not user:
        flash("Username tidak ditemukan")
    elif user[2] != hash_password(password):
        flash("Password salah")
    else:
        session["username"] = username
        return redirect("/profile")
    return redirect('/')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        file = request.files['photo']

        if not username or not password:
            flash("Data tidak boleh kosong.")
            return redirect('/register')

        if get_user(username):
            flash("Username sudah terdaftar.")
            return redirect('/register')

        if password.islower() or password.isupper() or password.isdigit():
            flash("Password kau jelek")
            return redirect('/register')

        if len(password) < 8 or not any(c.isupper() for c in password) or not any(c.isdigit() for c in password):
            flash("Password harus 8 huruf dan kombinasi angka, huruf besar & kecil")
            return redirect('/register')

        if "luthfi" in username.lower():
            flash("luthfi ganteng")
        elif "luwi" in username.lower():
            flash("luwi ganteng")
        else:
            flash("kurang apa yaaaa")

        filename = ""
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        with sqlite3.connect(DB_FILE) as conn:
            conn.execute("INSERT INTO users (username, password, photo, created_at) VALUES (?, ?, ?, ?)",
                         (username, hash_password(password), filename, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        flash("Registrasi berhasil!")
        return redirect('/')
    return render_template("register.html")

@app.route('/profile')
def profile():
    if "username" not in session:
        return redirect('/')
    user = get_user(session["username"])
    return render_template("profile.html", user=user)

@app.route('/logout')
def logout():
    session.pop("username", None)
    return redirect('/')

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    init_db()
    app.run(debug=True, host='0.0.0.0')