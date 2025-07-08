from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3, os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'secret'
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'

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

@app.route('/')
def index():
    conn = sqlite3.connect('phones.db')
    phones = conn.execute("SELECT id, brand, model, image FROM phones").fetchall()
    conn.close()
    return render_template('index.html', phones=phones)

@app.route('/phone/<int:phone_id>')
def phone_detail(phone_id):
    conn = sqlite3.connect('phones.db')
    phone = conn.execute("SELECT * FROM phones WHERE id=?", (phone_id,)).fetchone()
    conn.close()
    return render_template('phone_detail.html', phone=phone)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == ADMIN_USERNAME and request.form['password'] == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('add_phone'))
        flash('Invalid login')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

@app.route('/add', methods=['GET', 'POST'])
def add_phone():
    if not session.get('admin'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        data = {field: request.form[field] for field in request.form}
        image = request.files['image']
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        data['image'] = filename

        conn = sqlite3.connect('phones.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO phones (
                brand, model, release_date, status, dimensions, weight, build, sim,
                display_type, display_size, display_resolution, display_protection,
                os, chipset, cpu, gpu,
                internal, card_slot,
                main_camera, main_features, main_video,
                selfie_camera, selfie_features, selfie_video,
                battery_type, charging,
                wlan, bluetooth, gps, nfc, usb,
                sensors, colors, price, image
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', tuple(data[field] for field in data))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add_phone.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
