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
    
    # Create users table for login functionality
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    # Insert default admin user if not exists
    c.execute("SELECT * FROM users WHERE username = 'admin'")
    if not c.fetchone():
        c.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin')")
    
    conn.commit()
    conn.close()

# Initialize database
init_db()

@app.route('/')
def index():
    conn = sqlite3.connect('phones.db')
    phones = conn.execute("SELECT id, brand, model, image FROM phones").fetchall()
    conn.close()
    return render_template('index.html', phones=phones)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('phones.db')
        user = conn.execute("SELECT * FROM users WHERE username = ? AND password = ?", 
                           (username, password)).fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out!', 'info')
    return redirect(url_for('index'))

@app.route('/phone/<int:phone_id>')
def phone_detail(phone_id):
    conn = sqlite3.connect('phones.db')
    phone = conn.execute("SELECT * FROM phones WHERE id = ?", (phone_id,)).fetchone()
    conn.close()
    
    if not phone:
        flash('Phone not found!', 'error')
        return redirect(url_for('index'))
    
    return render_template('phone_detail.html', phone=phone)

@app.route('/add_phone', methods=['GET', 'POST'])
def add_phone():
    # Check if user is logged in
    if 'user_id' not in session:
        flash('Please login to add a phone!', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Handle file upload
        image_filename = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_filename = filename
        
        # Get form data
        brand = request.form.get('brand')
        model = request.form.get('model')
        release_date = request.form.get('release_date')
        status = request.form.get('status')
        dimensions = request.form.get('dimensions')
        weight = request.form.get('weight')
        build = request.form.get('build')
        sim = request.form.get('sim')
        display_type = request.form.get('display_type')
        display_size = request.form.get('display_size')
        display_resolution = request.form.get('display_resolution')
        display_protection = request.form.get('display_protection')
        os = request.form.get('os')
        chipset = request.form.get('chipset')
        cpu = request.form.get('cpu')
        gpu = request.form.get('gpu')
        internal = request.form.get('internal')
        card_slot = request.form.get('card_slot')
        main_camera = request.form.get('main_camera')
        main_features = request.form.get('main_features')
        main_video = request.form.get('main_video')
        selfie_camera = request.form.get('selfie_camera')
        selfie_features = request.form.get('selfie_features')
        selfie_video = request.form.get('selfie_video')
        battery_type = request.form.get('battery_type')
        charging = request.form.get('charging')
        wlan = request.form.get('wlan')
        bluetooth = request.form.get('bluetooth')
        gps = request.form.get('gps')
        nfc = request.form.get('nfc')
        usb = request.form.get('usb')
        sensors = request.form.get('sensors')
        colors = request.form.get('colors')
        price = request.form.get('price')
        
        # Insert into database
        conn = sqlite3.connect('phones.db')
        conn.execute('''
            INSERT INTO phones (
                brand, model, release_date, status, dimensions, weight, build, sim,
                display_type, display_size, display_resolution, display_protection,
                os, chipset, cpu, gpu, internal, card_slot, main_camera, main_features,
                main_video, selfie_camera, selfie_features, selfie_video, battery_type,
                charging, wlan, bluetooth, gps, nfc, usb, sensors, colors, price, image
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            brand, model, release_date, status, dimensions, weight, build, sim,
            display_type, display_size, display_resolution, display_protection,
            os, chipset, cpu, gpu, internal, card_slot, main_camera, main_features,
            main_video, selfie_camera, selfie_features, selfie_video, battery_type,
            charging, wlan, bluetooth, gps, nfc, usb, sensors, colors, price, image_filename
        ))
        conn.commit()
        conn.close()
        
        flash('Phone added successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('add_phone.html')

@app.route('/edit_phone/<int:phone_id>', methods=['GET', 'POST'])
def edit_phone(phone_id):
    # Check if user is logged in
    if 'user_id' not in session:
        flash('Please login to edit a phone!', 'error')
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('phones.db')
    
    if request.method == 'POST':
        # Handle file upload
        image_filename = request.form.get('current_image')  # Keep current image by default
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_filename = filename
        
        # Get form data and update database
        brand = request.form.get('brand')
        model = request.form.get('model')
        release_date = request.form.get('release_date')
        status = request.form.get('status')
        dimensions = request.form.get('dimensions')
        weight = request.form.get('weight')
        build = request.form.get('build')
        sim = request.form.get('sim')
        display_type = request.form.get('display_type')
        display_size = request.form.get('display_size')
        display_resolution = request.form.get('display_resolution')
        display_protection = request.form.get('display_protection')
        os = request.form.get('os')
        chipset = request.form.get('chipset')
        cpu = request.form.get('cpu')
        gpu = request.form.get('gpu')
        internal = request.form.get('internal')
        card_slot = request.form.get('card_slot')
        main_camera = request.form.get('main_camera')
        main_features = request.form.get('main_features')
        main_video = request.form.get('main_video')
        selfie_camera = request.form.get('selfie_camera')
        selfie_features = request.form.get('selfie_features')
        selfie_video = request.form.get('selfie_video')
        battery_type = request.form.get('battery_type')
        charging = request.form.get('charging')
        wlan = request.form.get('wlan')
        bluetooth = request.form.get('bluetooth')
        gps = request.form.get('gps')
        nfc = request.form.get('nfc')
        usb = request.form.get('usb')
        sensors = request.form.get('sensors')
        colors = request.form.get('colors')
        price = request.form.get('price')
        
        conn.execute('''
            UPDATE phones SET
                brand=?, model=?, release_date=?, status=?, dimensions=?, weight=?, build=?, sim=?,
                display_type=?, display_size=?, display_resolution=?, display_protection=?,
                os=?, chipset=?, cpu=?, gpu=?, internal=?, card_slot=?, main_camera=?, main_features=?,
                main_video=?, selfie_camera=?, selfie_features=?, selfie_video=?, battery_type=?,
                charging=?, wlan=?, bluetooth=?, gps=?, nfc=?, usb=?, sensors=?, colors=?, price=?, image=?
            WHERE id=?
        ''', (
            brand, model, release_date, status, dimensions, weight, build, sim,
            display_type, display_size, display_resolution, display_protection,
            os, chipset, cpu, gpu, internal, card_slot, main_camera, main_features,
            main_video, selfie_camera, selfie_features, selfie_video, battery_type,
            charging, wlan, bluetooth, gps, nfc, usb, sensors, colors, price, image_filename, phone_id
        ))
        conn.commit()
        conn.close()
        
        flash('Phone updated successfully!', 'success')
        return redirect(url_for('phone_detail', phone_id=phone_id))
    
    # GET request - show edit form
    phone = conn.execute("SELECT * FROM phones WHERE id = ?", (phone_id,)).fetchone()
    conn.close()
    
    if not phone:
        flash('Phone not found!', 'error')
        return redirect(url_for('index'))
    
    return render_template('edit_phone.html', phone=phone)

@app.route('/delete_phone/<int:phone_id>', methods=['POST'])
def delete_phone(phone_id):
    # Check if user is logged in
    if 'user_id' not in session:
        flash('Please login to delete a phone!', 'error')
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('phones.db')
    conn.execute("DELETE FROM phones WHERE id = ?", (phone_id,))
    conn.commit()
    conn.close()
    
    flash('Phone deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/search')
def search():
    query = request.args.get('q', '')
    if query:
        conn = sqlite3.connect('phones.db')
        phones = conn.execute(
            "SELECT id, brand, model, image FROM phones WHERE brand LIKE ? OR model LIKE ?",
            (f'%{query}%', f'%{query}%')
        ).fetchall()
        conn.close()
    else:
        phones = []
    
    return render_template('search.html', phones=phones, query=query)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
