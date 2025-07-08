from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3, os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'secret'
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def init_db():
    conn = sqlite3.connect('phones.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS phones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand TEXT,
            model TEXT,
            release_date TEXT,
            status TEXT,
            dimensions TEXT,
            weight TEXT,
            build TEXT,
            sim TEXT,
            display_type TEXT,
            display_size TEXT,
            display_resolution TEXT,
            display_protection TEXT,
            os TEXT,
            chipset TEXT,
            cpu TEXT,
            gpu TEXT,
            internal TEXT,
            card_slot TEXT,
            main_camera TEXT,
            main_features TEXT,
            main_video TEXT,
            selfie_camera TEXT,
            selfie_features TEXT,
            selfie_video TEXT,
            battery_type TEXT,
            charging TEXT,
            wlan TEXT,
            bluetooth TEXT,
            gps TEXT,
            nfc TEXT,
            usb TEXT,
            sensors TEXT,
            colors TEXT,
            price TEXT,
            image TEXT
        )
    ''')
    conn.commit()
    conn.close()

# 🧠 THIS IS THE CRUCIAL FIX
init_db()

@app.route('/')
def index():
    conn = sqlite3.connect('phones.db')
    phones = conn.execute("SELECT id, brand, model, image FROM phones").fetchall()
    conn.close()
    return render_template('index.html', phones=phones)

# ... (rest of your Flask routes like login, add_phone, etc.)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
