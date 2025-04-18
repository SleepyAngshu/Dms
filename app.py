from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
import mysql.connector
from datetime import datetime


app= Flask(__name__, template_folder="templates") #Defining the templates folder
app.secret_key = 'your_secret_key_here'
#MySQL Database Configuration (XAMPP)
db_config= {
    'host':'127.0.0.1',
    'user' : 'root',
    'password': '',
    'database': 'dms'
}


#Establising db connection
def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def register():
    return render_template('register.html')

#Session setup
@app.route('/set_session')
def set_session():
    #p_id = session.get('p_id')
    session['p_id'] = 1
    return 'Session set!'

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/food_intake_checker')
def food_intake_checker():
    return render_template('food_intake_checker.html')


@app.route('/patient_dashboard')
def patient_dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    #if 'p_id' not in session:
        #flash("Session timed out. Please login again.")
        #return redirect(url_for('register'))  # Add your login route

    p_id = 1 #########session['p_id'] 
    cursor.execute("""
        SELECT name, gl_b_breakfast, gl_a_breakfast, gl_b_lunch, gl_b_dinner, updated_on
        FROM patient
        WHERE p_id = %s
    """, (p_id,))
    patient = cursor.fetchone()

    conn.close()

    if not patient:
        return "Patient not found", 404
    
    glucose_data = [
        patient.get('gl_b_breakfast', 0),
        patient.get('gl_a_breakfast', 0),
        patient.get('gl_b_lunch', 0),
        patient.get('gl_b_dinner', 0)
    ]
    return render_template(
        'patient_dashboard.html',
        name=patient['name'],
        p_id=p_id,
        updated_on=patient['updated_on'],
        glucose_data=glucose_data
    )

    #return render_template(
        #patient_dashboard.html', **patient, p_id=p_id)
        #name=patient['name'],
        #p_id=p_id,
        #gl_b_breakfast=patient['gl_b_breakfast'],
        #gl_a_breakfast=patient['gl_a_breakfast'],
        #gl_b_lunch=patient['gl_b_lunch'],
        #gl_b_dinner=patient['gl_b_dinner'],
        #updated_on=patient['updated_on']
    #)





@app.route('/update_patient_profile', methods=['GET', 'POST'])
def update_patient_profile():
    #if 'p_id' not in session:
        #flash("Session timed out. Please login again.")
        #return redirect(url_for('register'))  # Add your login route

    p_id = 1 #########session['p_id'] 
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch existing values
    cursor.execute("""
        SELECT name, dob, weight, gender,
               gl_b_breakfast, gl_a_breakfast, gl_b_lunch, gl_b_dinner
        FROM patient WHERE p_id = %s
    """, (p_id,))
    patient = cursor.fetchone()

    if not patient:
        flash("No data found for this patient.")
        return redirect('/update_patient_profile')

    if request.method == 'POST':
        # Form values
        #name = request.form['name']
        dob = request.form['dob']
        weight = request.form['weight']
        gender = request.form['gender']
        gl_b_breakfast = request.form['gl_b_breakfast']
        gl_a_breakfast = request.form['gl_a_breakfast']
        gl_b_lunch = request.form['gl_b_lunch']
        gl_b_dinner = request.form['gl_b_dinner']

        # Determine if glucose values changed
        values_changed = (
            float(gl_b_breakfast) != float(patient['gl_b_breakfast']) or
            float(gl_a_breakfast) != float(patient['gl_a_breakfast']) or
            float(gl_b_lunch) != float(patient['gl_b_lunch']) or
            float(gl_b_dinner) != float(patient['gl_b_dinner'])
        )

        updated_on = datetime.now() if values_changed else patient.get('updated_on')

        # Update query
        cursor.execute("""
            UPDATE patient SET
                dob = %s,
                weight = %s,
                gender = %s,
                gl_b_breakfast = %s,
                gl_a_breakfast = %s,
                gl_b_lunch = %s,
                gl_b_dinner = %s,
                updated_on = %s
            WHERE p_id = %s
        """, (dob, weight, gender, gl_b_breakfast, gl_a_breakfast, gl_b_lunch, gl_b_dinner, updated_on, p_id))

        conn.commit() #changes in DB will be saved
        cursor.close()
        conn.close()

        flash("Profile successfully updated!")
        return redirect('/patient_dashboard')
    cursor.close()
    conn.close()
    return render_template('update_patient_profile.html', patient=patient)

    #print("update_patient_profile")
    #return render_template("update_patient_profile.html")



@app.route('/verified_doctor_list')
def verified_doctor_list():
    #if 'p_id' not in session:
        #flash("Session timed out. Please login again.")
        #return redirect(url_for('register'))  # Add your login route
    p_id=1 #remove this line while finalizing
    #p_id = session['p_id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT d_id, name, designation, location, email, phone 
        FROM doctor 
        WHERE verified = 1 AND designation IS NOT NULL 
        AND location IS NOT NULL AND phone IS NOT NULL
    """)
    doctor = cursor.fetchall()
    conn.close()
    
    return render_template('verified_doctor_list.html', doctor=doctor)


@app.route('/my_prescription')
def my_prescription():
    #if 'p_id' not in session:
        #flash("Session timed out. Please login again.")
        #return redirect(url_for('register'))  # Add your login route
    p_id=1 #remove this line while finalizing

    #p_id = session['p_id']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT pres_id, d_id, detail, date FROM prescription WHERE p_id = %s", (p_id,))
    prescriptions = cursor.fetchall()

    # Fetch doctor names for each prescription
    for prescription in prescriptions:
        cursor.execute("SELECT name FROM doctor WHERE d_id = %s", (prescription['d_id'],))
        doctor = cursor.fetchone()
        prescription['doctor_name'] = doctor['name'] if doctor else 'Unknown Doctor'

    cursor.close()
    conn.close()

    return render_template('my_prescription.html', prescriptions=prescriptions)
    

@app.route('/my_appointment')
def my_appointment():
    #if 'p_id' not in session:
        #flash("Session timed out. Please login again.")
        #return redirect(url_for('register'))  # Add your login route
    p_id=1 #remove this line while finalizing
    #p_id = session['p_id']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)    

    #Fetching appointments
    cursor.execute("SELECT app_id, d_id, date, time, confirmation, checked FROM appointment WHERE p_id = %s", (p_id,))
    appointments = cursor.fetchall()

    # Attaching doctor names
    for appointment in appointments:
        cursor.execute("SELECT name FROM doctor WHERE d_id = %s", (appointment['d_id'],))
        doc = cursor.fetchone()
        appointment['doctor_name'] = doc['name'] if doc else 'Unknown Doctor'

    cursor.close()
    conn.close()

    return render_template('my_appointment.html', appointments=appointments)


@app.route('/logout')
def logout():
    print("logout Pg")
    # Your logic for updating goes here
    return render_template('logout.html')

@app.route('/make_appointment')
def make_appointment():
    print("Make Appointment Pg")
    # Your logic for updating goes here
    return render_template('make_appointment.html')


#food_intake_checker
@app.route('/check_food')
def check_food():
    food_item = request.args.get('food_item')
    gender = request.args.get('gender')
    message = ""

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT Sugar_level FROM sugar_lvl WHERE Food = %s", (food_item,))
    result = cursor.fetchone()

    if result and gender:
        sugar_level = result['Sugar_level']

        if gender.lower() == 'male':
            if sugar_level > 38:
                message = f"{food_item} has {sugar_level}g sugar. Dangerous for male patients."
            elif 17 <= sugar_level <= 37.99:
                message = f"{food_item} has {sugar_level}g sugar. Moderately risky for male patients."
            else:
                message = f"{food_item} has {sugar_level}g sugar. Safe for male patients."
        elif gender.lower() == 'female':
            if sugar_level > 25:
                message = f"{food_item} has {sugar_level}g sugar. Dangerous for female patients."
            elif 12 <= sugar_level <= 24.99:
                message = f"{food_item} has {sugar_level}g sugar. Moderately risky for female patients."
            else:
                message = f"{food_item} has {sugar_level}g sugar. Safe for female patients."
        else:
            message = "Invalid gender. Please specify male or female."
    else:
        message = f"No data found for '{food_item}'."

    cursor.close()
    conn.close()

    return render_template('food_intake_checker.html', message=message)

from flask import request, render_template
import mysql.connector


#SOS
from flask import redirect, url_for

@app.route('/fire_sos', methods=['POST'])
def fire_sos():
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    # Temporary mock until login session is active
    p_id = 2 

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get name from patient profile
    cursor.execute("SELECT name FROM patient WHERE p_id = %s", (p_id,))
    patient = cursor.fetchone()

    if not patient:
        cursor.close()
        conn.close()
        return "Patient not found", 404

    name = patient['name']
    location = f"{latitude},{longitude}"

    # Store into sos_alerts table
    cursor.execute("""
        REPLACE INTO sos_alerts (p_id, name, location)
        VALUES (%s, %s, %s)
    """, (p_id, name, location))


    conn.commit()
    cursor.close()
    conn.close()

    return '', 204  




if __name__ == '__main__':
    app.run(debug=True)