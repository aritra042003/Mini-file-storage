import os
import sqlite3
import string
import random
from datetime import datetime, timedelta
from flask import Flask, request, redirect, url_for, render_template, send_from_directory, abort
from werkzeug.utils import secure_filename
import config

app = Flask(__name__)
app.config.from_object(config)

DB_NAME = "database.db"

# ------------------- Helper Functions -------------------

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        short_code TEXT UNIQUE NOT NULL,
        filename TEXT NOT NULL,
        filepath TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        expiry TIMESTAMP,
        downloads INTEGER DEFAULT 0
    )
    """)
    conn.commit()
    conn.close()

def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

# ------------------- Routes -------------------

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            return render_template("error.html", message="No file part")
        
        file = request.files["file"]
        if file.filename == "":
            return render_template("error.html", message="No selected file")

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            short_code = generate_short_code()

            # Save file with short_code prefix to avoid conflicts
            saved_filename = f"{short_code}_{filename}"
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], saved_filename)
            file.save(filepath)

            # Expiry: 1 day from now
            expiry_time = datetime.now() + timedelta(days=1)

            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("INSERT INTO files (short_code, filename, filepath, expiry) VALUES (?, ?, ?, ?)",
                      (short_code, filename, filepath, expiry_time))
            conn.commit()
            conn.close()

            return render_template("success.html", short_code=short_code)

        else:
            return render_template("error.html", message="File type not allowed")

    return render_template("index.html")

@app.route("/download/<short_code>")
def download(short_code):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT filename, filepath, expiry, downloads FROM files WHERE short_code=?", (short_code,))
    row = c.fetchone()
    conn.close()

    if not row:
        return render_template("error.html", message="File not found")

    filename, filepath, expiry, downloads = row

    # ✅ Check expiry safely
    if expiry:
        try:
            expiry_dt = datetime.fromisoformat(expiry)  # handles microseconds automatically
            if expiry_dt < datetime.now():
                return render_template("error.html", message="File expired")
        except Exception:
            return render_template("error.html", message="Invalid expiry format")

    # ✅ Update download count
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE files SET downloads = downloads + 1 WHERE short_code=?", (short_code,))
    conn.commit()
    conn.close()

    return send_from_directory(os.path.dirname(filepath), os.path.basename(filepath), as_attachment=True)


# ------------------- Main -------------------

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
