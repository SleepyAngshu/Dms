from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key in production

# MySQL Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # XAMPP's default MySQL password is empty
    'database': 'dms'
}

# Create database connection
def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn, conn.cursor(dictionary=True)

# Login required decorator - ONLY DEFINE THIS ONCE
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Please login to access this page', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
        
    return decorated_function

# Routes - ONLY DEFINE EACH ROUTE ONCE
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn, cursor = get_db_connection()
        cursor.execute('SELECT * FROM admin WHERE email = %s AND password = %s', (email, password))
        admin = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if admin:
            session['admin_id'] = admin['id']
            session['email'] = admin['email']
            flash('Login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')

@app.route('/admin')
@login_required
def admin_dashboard():
    conn, cursor = get_db_connection()
    
    # Get pending doctor verifications
    cursor.execute("SELECT COUNT(*) AS pending_count FROM doctor WHERE verified = 0")
    pending_count = cursor.fetchone()['pending_count']
    
    # Get today's appointments
    cursor.execute("SELECT COUNT(*) AS pending_app FROM appointment WHERE DATE(date) = CURDATE()")
    pending_app = cursor.fetchone()['pending_app']
    
    # Get total doctors count
    cursor.execute("SELECT COUNT(*) AS total_doctors FROM doctor")
    total_doctors = cursor.fetchone()['total_doctors']
    
    # Get total patients count
    cursor.execute("SELECT COUNT(*) AS total_patients FROM patient")
    total_patients = cursor.fetchone()['total_patients']
    
    cursor.close()
    conn.close()
    
    # Get current timestamp using only datetime (no pytz)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    return render_template('admin.html', 
                          email=session.get('email'),
                          pending_count=pending_count,
                          pending_app=pending_app,
                          total_doctors=total_doctors,
                          total_patients=total_patients,
                          timestamp=timestamp)

@app.route('/admin/doctors')
@login_required
def admin_doctors():
    conn, cursor = get_db_connection()
    cursor.execute("SELECT * FROM doctor")
    doctors = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('addoc.html', doctors=doctors)

@app.route('/admin/verify', methods=['GET', 'POST'])
@login_required
def admin_verify():
    if request.method == 'POST':
        d_id = request.form['d_id']
        action = request.form['action']
        
        conn, cursor = get_db_connection()
        
        if action == 'Confirm':
            cursor.execute("UPDATE doctor SET verified = 1 WHERE d_id = %s", (d_id,))
            flash(f'Doctor ID {d_id} has been verified successfully!', 'success')
        elif action == 'Cancel':
            cursor.execute("UPDATE doctor SET verified = 2 WHERE d_id = %s", (d_id,))
            flash(f'Doctor ID {d_id} verification has been cancelled.', 'warning')
            
        conn.commit()
        cursor.close()
        conn.close()
        
        # Redirect to the same page with the fragment
        return redirect(url_for('admin_verify', _anchor=f'doctor{d_id}'))
    
    conn, cursor = get_db_connection()
    # Get all doctors, ordered by verification status (pending first)
    cursor.execute("SELECT * FROM doctor ORDER BY verified ASC, d_id ASC")
    doctors = cursor.fetchall()
    
    # Get count of pending verifications
    cursor.execute("SELECT COUNT(*) AS pending_count FROM doctor WHERE verified = 0")
    pending_count = cursor.fetchone()['pending_count']
    
    cursor.close()
    conn.close()
    
    return render_template('adverify.html', doctors=doctors, pending_count=pending_count)

@app.route('/admin/appointments')
@login_required
def admin_appointments():
    conn, cursor = get_db_connection()
    # Join with doctor and patient tables to get names
    cursor.execute("""
        SELECT a.*, d.name as doctor_name, p.name as patient_name 
        FROM appointment a
        JOIN doctor d ON a.d_id = d.d_id
        JOIN patient p ON a.p_id = p.p_id
        ORDER BY a.date DESC, a.time DESC
    """)
    appointments = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('adappoin.html', appointments=appointments)

@app.route('/admin/patients')
@login_required
def admin_patients():
    conn, cursor = get_db_connection()
    cursor.execute("SELECT * FROM patient")
    patients = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('adpatients.html', patients=patients)

@app.route('/admin/prescriptions')
@login_required
def admin_prescriptions():
    conn, cursor = get_db_connection()
    # Join with doctor and patient tables to get names
    cursor.execute("""
        SELECT p.*, d.name as doctor_name, pt.name as patient_name 
        FROM prescription p
        JOIN doctor d ON p.d_id = d.d_id
        JOIN patient pt ON p.p_id = pt.p_id
        ORDER BY p.date DESC
    """)
    prescriptions = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('adprescriptions.html', prescriptions=prescriptions)

@app.route('/admin/appointment/update', methods=['POST'])
@login_required
def update_appointment():
    if request.method == 'POST':
        app_id = request.form['app_id']
        action = request.form['action']
        
        conn, cursor = get_db_connection()
        
        if action == 'Confirm':
            cursor.execute("UPDATE appointment SET confirmation = 1 WHERE app_id = %s", (app_id,))
            flash(f'Appointment ID {app_id} has been confirmed!', 'success')
        elif action == 'Cancel':
            cursor.execute("UPDATE appointment SET confirmation = 2 WHERE app_id = %s", (app_id,))
            flash(f'Appointment ID {app_id} has been cancelled.', 'warning')
        elif action == 'Mark Checked':
            cursor.execute("UPDATE appointment SET checked = 1 WHERE app_id = %s", (app_id,))
            flash(f'Appointment ID {app_id} has been marked as checked.', 'success')
            
        conn.commit()
        cursor.close()
        conn.close()
        
        return redirect(url_for('admin_appointments'))

# ONLY DEFINE LOGOUT ONCE
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)