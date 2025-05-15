#OUR MAIN UPDATED VERSION


from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
import mysql.connector
from datetime import datetime
from datetime import datetime, timedelta
from datetime import date
from functools import wraps
import re


# Import models
from models.user_model import login_user, register_user, validate_email
from models.admin_model import get_dashboard_stats, get_all_doctors, get_all_doctors_for_verification, update_doctor_verification
from models.appointment_model import get_all_appointments, get_all_prescriptions
from models.pharmacy_model import get_all_pharmacies, get_nearby_pharmacies
from models.medicine_model import get_medicines_by_pharmacy, add_medicine, update_medicine, delete_medicine
from models.sos_model import get_all_sos_alerts

from models.order_medicine import search_medicines_by_name, create_order
from models.review_model import add_review, get_patient_reviews, delete_review, get_reviewable_doctors,get_doctor_reviews
from models.admin_model import get_all_orders, update_order_status
from models.sos_model import update_sos_alert_status

from models.patient_model import get_patient_name_glucose_info_update, get_patient_details, update_patient_details
from models.patient_model import get_verified_doctor_details,get_patient_prescription, get_doctor_name_for_each_prescription
from models.patient_model import get_appointment_details, get_doctor_name_for_each_appointment, filter_doctor_by_area
from models.patient_model import get_distinct_area, get_patient_required_fields, get_doctor_schedule,get_diet_plan_by_age_and_gender
from models.patient_model import check_existing_appointment, insert_appointment, get_column_value, insert_sos_alert,is_duplicate_telemedicine,get_food_sugar_level
from models.patient_model import get_patient_notifications, get_time_based_medication_reminder,get_patient_notifications, dismiss_patient_notification
from models.appointment_model import insert_telemedicine_payment

from models.doctor_model import get_doctor_by_id, update_doctor_profile, get_doctor_name, update_doctor_schedule, get_doctor_schedule, get_pending_appointments, update_appointment_status, insert_prescription, check_patient_appointment
from models.admin_model import insert_notice
from models.doctor_model import get_doctor_notices 
from models.patient_model import get_patient_notices

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



#####################################################################3
def get_upcoming_week_days(available_days):
    today = datetime.today()
    result = []

    for i in range(1, 8):  # Check next 1 week
        day_date = today + timedelta(days=i)
        day_name = day_date.strftime('%A')

        if day_name in available_days:
            result.append({
                'day': day_name,
                'date': day_date.strftime('%Y-%m-%d'),
                'formatted': day_date.strftime('%d %B %Y')  # 21 April 2025
            })
    print("result:", result)
    return result
def get_day(date):
    date_string = str(date)  
    date_object = datetime.strptime(date_string, '%Y-%m-%d')  #convert to datetime
    day_name = date_object.strftime('%A')  #gets the full day name
    day = day_name.lower()
    return day  


# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return redirect(url_for('login'))




############ ADI ############
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['user']  # 'Doctor' or 'Patient'
        
        # Basic validation
        if not username or not email or not password or not role:
            flash('All fields are required', 'error')
            return redirect(url_for('register'))
        
        # Email validation
        if not validate_email(email):
            flash('Please enter a valid email address', 'error')
            return redirect(url_for('register'))
        
        # Password validation (at least 6 characters)
        if len(password) < 3:
            flash('Password must be at least 6 characters long', 'error')
            return redirect(url_for('register'))
        
        # Register user
        result = register_user(username, email, password, role)
        
        if result['success']:
            flash(result['message'], 'success')
            return redirect(url_for('login'))
        else:
            flash(result['message'], 'error')
            return redirect(url_for('register'))
    
    return render_template('register.html')


# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        
        user_data = login_user(email, password, role)
        
        if user_data:
            # Store user data in session
            session['user_id'] = user_data['user_id']
            session['email'] = user_data['email']
            session['role'] = user_data['role']
            session['name'] = user_data['name']
            
            flash('Login successful!', 'success')
            
            # Redirect based on role
            if role == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif role == 'doctor':
                return redirect(url_for('doctor_dashboard'))
            elif role == 'patient':
                return redirect(url_for('patient_dashboard'))
        
        flash('Invalid email, password, or role selection', 'error')
    
    return render_template('login.html')

#######################
#Session setup

# @app.route('/patient_dashboard', endpoint= 'patient_dashboard') ##removed for angshu
# def patient_dashboard():
#     p_id= session['user_id']
#     #p_id = session['p_id']
#     # p_id = 1 
#     if 'user_id' not in session:  #######Finally activate this
#         flash("Session timed out. Please login again.")
#         return redirect(url_for('login'))  # Add your login route

    

#     patient = get_patient_name_glucose_info_update(p_id)
#     if not patient:
#         return "Patient not found", 404
    
#     glucose_data = [
#         patient.get('gl_b_breakfast', 0),
#         patient.get('gl_a_breakfast', 0),
#         patient.get('gl_b_lunch', 0),
#         patient.get('gl_b_dinner', 0)
#     ]
#     return render_template(
#         'patient_dashboard.html',
#         name=patient['name'],
#         p_id=p_id,
#         updated_on=patient['updated_on'],
#         glucose_data=glucose_data
#     )

#new patient dashboard angshu

# Inside your existing /patient_dashboard route


@app.route('/patient_dashboard', endpoint='patient_dashboard')
def patient_dashboard():
    if 'user_id' not in session:
        flash("Session timed out. Please login again.")
        return redirect(url_for('login'))

    p_id = session['user_id']

    patient = get_patient_name_glucose_info_update(p_id)
    if not patient:
        return "Patient not found", 404

    glucose_data = [
        patient.get('gl_b_breakfast', 0),
        patient.get('gl_a_breakfast', 0),
        patient.get('gl_b_lunch', 0),
        patient.get('gl_b_dinner', 0)
    ]
    
    notices = get_patient_notices(p_id)  # ✅ Fetch notices for this patient - nahian m4
    notifications = get_patient_notifications(p_id)  # 🆕 fetch notifications angshu for doctor appointment confirm/cancel/reschedule
    # 🆕 Medication reminder message angshu for reminder
    medication_message = get_time_based_medication_reminder(p_id)

    # return render_template(
    #     'patient_dashboard.html',
    #     name=patient['name'],
    #     p_id=p_id,
    #     updated_on=patient['updated_on'],
    #     glucose_data=glucose_data,
    #     notifications=notifications,
    #     medication_message=medication_message
    #     notices=notices)  # Pass to view
    return render_template('patient_dashboard.html', name=patient['name'], p_id=p_id, updated_on=patient['updated_on'], glucose_data=glucose_data, notifications=notifications, medication_message=medication_message, notices=notices)

@app.route('/dismiss_notification/<int:notif_id>', methods=['POST'])
def dismiss_notification(notif_id):
    dismiss_patient_notification(notif_id)
    return '', 204




@app.route('/update_patient_profile', methods=['GET', 'POST'])
def update_patient_profile():
    p_id= session['user_id']
   
    if 'user_id' not in session:
        flash("Session timed out. Please login again.")
        return redirect(url_for('login')) 
    
 

    #fetching patient details
    patient = get_patient_details(p_id)

    if not patient:
        flash("No data found for this patient.")
        return redirect('/update_patient_profile')

    if request.method == 'POST':
        # Form values
        dob = request.form['dob']
        phone = request.form['phone']
        weight = request.form['weight']
        gender = request.form['gender']
        gl_b_breakfast = request.form['gl_b_breakfast']
        gl_a_breakfast = request.form['gl_a_breakfast']
        gl_b_lunch = request.form['gl_b_lunch']
        gl_b_dinner = request.form['gl_b_dinner']

        #Checking if glucose values changed
        values_changed = (
            float(gl_b_breakfast) != float(patient['gl_b_breakfast']) or
            float(gl_a_breakfast) != float(patient['gl_a_breakfast']) or
            float(gl_b_lunch) != float(patient['gl_b_lunch']) or
            float(gl_b_dinner) != float(patient['gl_b_dinner'])
        )
        updated_on = datetime.now() if values_changed else patient.get('updated_on')
        
        update_patient_details(dob, phone, weight, gender, gl_b_breakfast, gl_a_breakfast, gl_b_lunch, gl_b_dinner, updated_on, p_id)
        
        if not patient:
            flash("No data found for this patient.")
            return redirect('/update_patient_profile')
        else:
            flash("Patient profile updated successfully")
            return redirect('/patient_dashboard')
    
    return render_template('update_patient_profile.html', patient=patient) 


################################   DOC REVIEW ########################

# @app.route('/verified_doctor_list')
# def verified_doctor_list():
#     p_id = session['user_id']
#     if 'user_id' not in session:
#         flash("Session timed out. Please login again.")
#         return redirect(url_for('login'))

#     area = request.args.get('area')
#     if area:
#         doctor = filter_doctor_by_area(area)
#     else:
#         doctor = get_verified_doctor_details()   
    
#     # Add this code to fetch reviews for each doctor
#     for doc in doctor:
#         doc['reviews'] = get_doctor_reviews(doc['d_id'])
    
#     distinct_area_lst = get_distinct_area()
#     return render_template('verified_doctor_list.html', doctor=doctor, areas=distinct_area_lst)  

# Modified verified_doctor_list to correctly handle review data structure
@app.route('/verified_doctor_list')
def verified_doctor_list():
    p_id = session['user_id']
    if 'user_id' not in session:
        flash("Session timed out. Please login again.")
        return redirect(url_for('login'))

    area = request.args.get('area')
    if area:
        doctor = filter_doctor_by_area(area)
    else:
        doctor = get_verified_doctor_details()   
    
    # Process reviews for each doctor
    for doc in doctor:
        # Get reviews data (which is a dictionary with reviews, avg_rating, and total_reviews)
        reviews_data = get_doctor_reviews(doc['d_id'])
        
        # Extract the actual reviews list from the dictionary
        doc['reviews'] = reviews_data.get('reviews', [])
        
        # Also add average rating and total reviews count
        doc['avg_rating'] = reviews_data.get('avg_rating', 0)
        doc['total_reviews'] = reviews_data.get('total_reviews', 0)
    
    distinct_area_lst = get_distinct_area()
    return render_template('verified_doctor_list.html', doctor=doctor, areas=distinct_area_lst)

######################  DOC REVIEW ENDS ##########################
@app.route('/my_prescription')
def my_prescription():

    p_id= session['user_id']
 
    if 'user_id' not in session:
        flash("Session timed out. Please login again.")
        return redirect(url_for('login'))  

   
    prescriptions = get_patient_prescription(p_id)
    print(prescriptions)

    # Fetch doctor names for each prescription
    for prescription in prescriptions:
        doctor = get_doctor_name_for_each_prescription(prescription)
        prescription['doctor_name'] = doctor['name'] if doctor else 'Unknown Doctor'
    return render_template('my_prescription.html', prescriptions=prescriptions)
    

@app.route('/my_appointment')
def my_appointment():
    p_id= session['user_id']
    
    if 'user_id' not in session:
        flash("Session timed out. Please login again.")
        return redirect(url_for('login'))  
   
    #Fetching appointments
    appointments = get_appointment_details(p_id)

    # Attaching doctor names
    for appointment in appointments:
        doc = get_doctor_name_for_each_appointment(appointment)
        appointment['doctor_name'] = doc['name'] if doc else 'Unknown Doctor'
    return render_template('my_appointment.html', appointments=appointments)



@app.route('/make_appointment')
def make_appointment():
    d_id = request.args.get('d_id')
    p_id= session['user_id']
   
    if 'user_id' not in session:
        flash("Session timed out. Please login again.")
        return redirect(url_for('login'))  

    if not d_id:
        return redirect('/verified_doctor_list')  

    patient = get_patient_required_fields(p_id)

    if not patient:
        return "Error: Patient not found.", 404

    required_fields = ['name', 'dob', 'weight', 'gender', 
                       'gl_b_breakfast', 'gl_a_breakfast', 
                       'gl_b_lunch', 'gl_b_dinner']

    is_profile_complete = all(
        patient.get(field) not in (None, '', 0.0) for field in required_fields
    )

    error = session.pop('error', {})
    post_data = session.pop('post_data', {})

    # --- Fetching Doctor's Schedule
    doctor_schedule= get_doctor_schedule(d_id)
    
    # Filtering available days (day=non-null values)
    available_days = []
    available_times = {}

    if doctor_schedule:
        

        for day, time_value in doctor_schedule.items():
            if day=='telemedicine_days':
                if time_value: #meaning telemedicine_days col isnt empty, it has a day in it
                    upcoming_telemedicine_day = get_upcoming_week_days(time_value)
                    

            else:
              if time_value:  # If not NULL
                available_days.append(day.capitalize()) 
                available_times[day] = str(time_value).split(',')

    # Generate upcoming dates for available days
    #print("Available Days:", available_days)

    upcoming_days = get_upcoming_week_days(available_days)
    #print("Upcoming Days:", upcoming_days)

    # Attach the correct time from available_times into upcoming_days list
    for day in upcoming_days:
        day_name = day['day'].lower()  # e.g. "monday"
        day['time'] = ', '.join(available_times.get(day_name, []))  # Fetch time string



    return render_template(
        'make_appointment.html',
        d_id=d_id,
        p_id=p_id,
        is_profile_complete=is_profile_complete,
        error=error,
        post_data=post_data,
        available_days=available_days,
        available_times=available_times,
        upcoming_days=upcoming_days,
        upcoming_telemedicine_day=upcoming_telemedicine_day 
    )

    

#new code angshu
@app.route('/make_appointment_process', methods=['POST'])
def make_appointment_process():
    if 'user_id' not in session:
        flash("Session timed out. Please login again.")
        return redirect(url_for('login'))

    p_id = session['user_id']
    d_id = request.form.get('d_id')
    date = request.form.get('date')
    appointment_type = request.form.get('appointment_type') 
    day = get_day(date)
    error = {}

    if appointment_type != 'telemedicine':
        time = get_column_value(d_id, day)
        appointment_exist = check_existing_appointment(p_id, date)
        if appointment_exist:
            error['appointment'] = "You cannot make more than 1 appointment on the same day."
    else:
        time = '20:00 - 22:00'
        if is_duplicate_telemedicine(p_id, date, time):
            error['appointment'] = "You cannot make more than 1 telemedicine appointment on the same day at the same time."

    if error:
        session['error'] = error
        session['post_data'] = request.form.to_dict()
        return redirect(f'/make_appointment?d_id={d_id}')

    if appointment_type == 'telemedicine':
        return redirect(url_for('telemedicine_payment', d_id=d_id, schedule=f"{date} {time}"))

    # Insert in-person appointment
    success = insert_appointment(d_id, p_id, date, time, appointment_type)
    return render_template('make_appointment_process.html', success=success)



@app.route('/fire_sos', methods=['POST'])
def fire_sos():
    p_id= session['user_id']
    
    if 'user_id' not in session:
        flash("Session timed out. Please login again.")
        return redirect(url_for('login'))  
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    patient = get_patient_details(p_id)

    if not patient:
        return "Patient not found", 404

    insert_sos_alert(p_id, patient['name'], latitude, longitude)

    return '', 204  # Silent success
    


#FOOD INTAKE CHECKER
@app.route('/food_intake_checker',methods=['GET', 'POST'])
def food_intake_checker():
    food_item = request.args.get('food_item')
    gender = request.args.get('gender')
    message = ""

    if food_item and gender:
        sugar_level = get_food_sugar_level(food_item)

        if sugar_level is not None:
            sugar_level = float(sugar_level)
            if gender == 'male':
                if sugar_level > 38:
                    message = "⚠️ This food is dangerous for male patients."
                elif 17 <= sugar_level <= 37.99:
                    message = "⚠️ This food is moderately risky for male patients."
                else:
                    message = "✅ This food is safe for male patients."
            elif gender == 'female':
                if sugar_level > 25:
                    message = "⚠️ This food is dangerous for female patients."
                elif 12 <= sugar_level <= 24.99:
                    message = "⚠️ This food is moderately risky for female patients."
                else:
                    message = "✅ This food is safe for female patients."
        else:
            message = "❌ Food item not found in database."

    return render_template("food_intake_checker.html", message=message)


############  ADI Admin   ###################

@app.route('/admin')
@login_required
def admin_dashboard():
    stats = get_dashboard_stats()
    return render_template('admin.html', 
                          email=session.get('email'),
                          pending_count=stats['pending_count'],
                          pending_app=stats['pending_app'],
                          total_doctors=stats['total_doctors'],
                          total_patients=stats['total_patients'],
                          timestamp=stats['timestamp'])

@app.route('/admin/doctors')
@login_required
def admin_doctors():
    doctors = get_all_doctors()
    return render_template('addoc.html', doctors=doctors)

@app.route('/admin/sos')
@login_required
def admin_sos():
    sos_alerts = get_all_sos_alerts()
    return render_template('adsos.html', sos_alerts=sos_alerts)

@app.route('/admin/verify', methods=['GET', 'POST'])
@login_required
def admin_verify():
    if request.method == 'POST':
        d_id = request.form['d_id']
        action = request.form['action']
        
        result = update_doctor_verification(d_id, action)
        
        if result['success']:
            flash(result['message'], 'success' if 'success' in result['message'] else 'warning')
        else:
            flash(result['message'], 'error')
        
        
        return redirect(url_for('admin_verify', _anchor=f'doctor{d_id}'))
    
    verification_data = get_all_doctors_for_verification()
    return render_template('adverify.html', 
                          doctors=verification_data['doctors'], 
                          pending_count=verification_data['pending_count'])

@app.route('/admin/appointments')
@login_required
def admin_appointments():
    appointments = get_all_appointments()
    return render_template('addapoin.html', appointments=appointments)

@app.route('/admin/prescriptions')
@login_required
def admin_prescriptions():
    prescriptions = get_all_prescriptions()
    return render_template('adprescriptions.html', prescriptions=prescriptions)

# @app.route('/admin/appointment/update', methods=['POST'])
# @login_required
# def update_appointment():
#     if request.method == 'POST':
#         app_id = request.form['app_id']
#         action = request.form['action']
        
#         result = update_appointment_status(app_id, action)
        
#         if result['success']:
#             flash(result['message'], 'success' if 'confirmed' in result['message'] or 'checked' in result['message'] else 'warning')
#         else:
#             flash(result['message'], 'error')
        
#         return redirect(url_for('admin_appointments'))

# Pharmacy routes
@app.route('/admin/pharmacy-locator')
@login_required
def branch_locator():
    return render_template('pharmacy_locator.html')

@app.route('/admin/get-pharmacies', methods=['GET'])
@login_required
def get_pharmacies():
    pharmacies = get_all_pharmacies()
    return jsonify(pharmacies)

@app.route('/admin/nearby-pharmacies', methods=['POST'])
@login_required
def nearby_pharmacies():
    data = request.json
    lat = data.get('lat')
    lng = data.get('lng')
    radius = data.get('radius', 5)  # Default 5km
    
    if not lat or not lng:
        return jsonify({'error': 'Latitude and longitude are required'}), 400
    
    pharmacies = get_nearby_pharmacies(lat, lng, radius)
    return jsonify(pharmacies)

# Medicine routes
@app.route('/admin/medicine-management')
@login_required
def medicine_management():
    return render_template('medicine_management.html')

@app.route('/admin/get-medicines/<int:pharmacy_id>')
@login_required
def get_medicines(pharmacy_id):
    medicines = get_medicines_by_pharmacy(pharmacy_id)
    
    if 'error' in medicines:
        return jsonify({"error": medicines['error']}), 500
    
    return jsonify(medicines)

@app.route('/admin/add-medicine', methods=['POST'])
@login_required
def add_medicine_route():
    data = request.json
    
    # Validate required fields
    if not data.get('medicine_name') or not data.get('pharmacy_id'):
        return jsonify({"error": "Medicine name and pharmacy ID are required"}), 400
    
    result = add_medicine(data)
    
    if result['success']:
        return jsonify({"success": True, "id": result['id']})
    else:
        return jsonify({"error": result['error']}), 500

@app.route('/admin/update-medicine', methods=['POST'])
@login_required
def update_medicine_route():
    data = request.json
    
    # Validate required fields
    if not data.get('medicine_id'):
        return jsonify({"error": "Medicine ID is required"}), 400
    
    result = update_medicine(data)
    
    if result['success']:
        return jsonify({"success": True})
    else:
        return jsonify({"error": result['error']}), 500

@app.route('/admin/delete-medicine', methods=['POST'])
@login_required
def delete_medicine_route():
    data = request.json
    
    # Validate required fields
    if not data.get('medicine_id'):
        return jsonify({"error": "Medicine ID is required"}), 400
    
    result = delete_medicine(data['medicine_id'])
    
    if result['success']:
        return jsonify({"success": True})
    else:
        return jsonify({"error": result['error']}), 500



# Adi integrated - Medicine ordering routes
@app.route('/order_medicine')
def order_medicine():
    return render_template('order_medicine.html')

# Adi integrated - Search medicines API
@app.route('/search_medicines')
def search_medicines_route():
    search_term = request.args.get('term', '')   
    # Search for medicines
    medicines = search_medicines_by_name(search_term)
    
    return jsonify(medicines)

# Adi integrated - Place order API
@app.route('/place_order', methods=['POST'])
def place_order():
    if 'user_id' not in session:
        return jsonify({"success": False, "error": "Please log in to place an order"})
    
    data = request.json
    p_id = session['user_id']
    
    items = data.get('items', [])
    delivery_address = data.get('delivery_address')
    
    if not items:
        return jsonify({"success": False, "error": "Your cart is empty"})
    
    if not delivery_address:
        return jsonify({"success": False, "error": "Please provide a delivery address"})
    
    # Additional data like payment method
    additional_data = {
        'payment_method': data.get('payment_method', 'cash')
    }
    
    # Create the order - removed pharmacy_id parameter
    result = create_order(p_id, items, delivery_address, additional_data)
    
    return jsonify(result)

# Adi integrated - Doctor review system
@app.route('/write_review', methods=['GET', 'POST'])
def write_review():
    if 'user_id' not in session:
        flash("Session timed out. Please login again.")
        return redirect(url_for('login'))
    
    p_id = session['user_id']
    
    if request.method == 'POST':
        d_id = request.form.get('d_id')
        rating = request.form.get('rating')
        comment = request.form.get('comment')
        
        if not d_id or not rating:
            flash("Doctor and rating are required", "error")
            return redirect(url_for('write_review'))
        
        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                flash("Rating must be between 1 and 5", "error")
                return redirect(url_for('write_review'))
        except ValueError:
            flash("Invalid rating value", "error")
            return redirect(url_for('write_review'))
        
        result = add_review(p_id, d_id, rating, comment)
        
        if result['success']:
            flash(result['message'], "success")
            return redirect(url_for('my_reviews'))
        else:
            flash(result['message'], "error")
            return redirect(url_for('write_review'))
    
    # GET request - show form
    reviewable_doctors = get_reviewable_doctors(p_id)
    return render_template('write_review.html', doctors=reviewable_doctors)

# Adi integrated - View patient's own reviews
@app.route('/my_reviews')
def my_reviews():
    if 'user_id' not in session:
        flash("Session timed out. Please login again.")
        return redirect(url_for('login'))
    
    p_id = session['user_id']
    reviews = get_patient_reviews(p_id)
    return render_template('my_reviews.html', reviews=reviews)

# Adi integrated - Delete review
@app.route('/delete_review/<int:review_id>', methods=['POST'])
def delete_review_route(review_id):
    if 'user_id' not in session:
        flash("Session timed out. Please login again.")
        return redirect(url_for('login'))
    
    p_id = session['user_id']
    result = delete_review(review_id, p_id)
    
    if result['success']:
        flash(result['message'], "success")
    else:
        flash(result['message'], "error")
    
    return redirect(url_for('my_reviews'))

# Adi integrated - Doctor view of their reviews
@app.route('/doctor_reviews')
def doctor_reviews():
    if 'user_id' not in session:
        flash("Session timed out. Please login again.")
        return redirect(url_for('login'))
    
    if session['role'] != 'doctor':
        flash("Access denied", "error")
        return redirect(url_for('index'))
    
    d_id = session['user_id']
    review_data = get_doctor_reviews(d_id)
    return render_template('doctor_reviews.html', review_data=review_data)

# Adi integrated - SOS response system for admin
@app.route('/respond_to_sos/<int:alert_id>', methods=['POST'])
@login_required
def respond_to_sos(alert_id):
    try:
        # Update the alert status in the database
        success = update_sos_alert_status(alert_id, responded=1)
        
        if success:
            return jsonify({'success': True, 'message': 'Alert status updated successfully'})
        else:
            return jsonify({'success': False, 'message': 'Alert not found or already responded'}), 404
    except Exception as e:
        print(f"Error updating SOS alert: {str(e)}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

# Adi integrated - Admin order management
@app.route('/admin/orders')
@login_required
def admin_orders():
    try:
        # Get orders and ensure it's a list
        orders = get_all_orders()
        
        # Debug information
        print(f"Type of orders: {type(orders)}")
        print(f"Number of orders: {len(orders) if isinstance(orders, list) else 'Not a list'}")
        
        # Ensure orders is a list
        if not isinstance(orders, list):
            print("Orders is not a list, converting to empty list")
            orders = []
        
        # Process each order to ensure all attributes are safe to use in the template
        for order in orders:
            # Ensure items is a list
            if not isinstance(order.get('items'), list):
                order['items'] = []
            
            # Ensure numeric values are of the right type
            if 'total_amount' not in order or not isinstance(order['total_amount'], (int, float)):
                order['total_amount'] = 0
                
            # Ensure all items have the right attributes
            for item in order.get('items', []):
                if 'price' not in item or not isinstance(item['price'], (int, float)):
                    item['price'] = 0
                if 'quantity' not in item or not isinstance(item['quantity'], int):
                    item['quantity'] = 0
        
        return render_template('adorders.html', orders=orders)
    except Exception as e:
        import traceback
        print(f"Error in admin_orders route: {str(e)}")
        print(traceback.format_exc())
        # Return an empty list if there's an error
        return render_template('adorders.html', orders=[])

# Adi integrated - Update order status
@app.route('/admin/order/update', methods=['POST'])
@login_required
def update_order():
    if request.method == 'POST':
        order_id = request.form['order_id']
        status = request.form['status']
        
        result = update_order_status(order_id, status)
        
        if result['success']:
            flash(result['message'], 'success')
        else:
            flash(result['message'], 'error')
        
        return redirect(url_for('admin_orders'))







######################  ADIOS FROM ADI :) ###########################



#==================== NAHIAN - doctor =========================

@app.route('/update_doctor_profile', methods=['GET', 'POST'], endpoint='update_doctor_profile')
def update_doctor_profile_route():
    d_id= session['user_id']
    if 'user_id' not in session:  #######Finally activate this
        flash("Session timed out. Please login again.")
        return redirect(url_for('login'))  # Add your login route
    
    if request.method == 'POST':
        designation = request.form['designation']
        phone = request.form['phone']
        location = request.form['location']

        update_doctor_profile(d_id, designation, phone, location)
        return redirect(url_for('doctor_dashboard'))

    doctor = get_doctor_by_id(d_id)
    if doctor:
        return render_template('update_doctor_profile.html', doctor=doctor)
    else:
        return 'Doctor not found', 404


@app.route('/doctor_dashboard', endpoint='doctor_dashboard')
def doctor_dashboard():
    d_id= session['user_id']
    if 'user_id' not in session:  #######Finally activate this
        flash("Session timed out. Please login again.")
        return redirect(url_for('login'))  # Add your login route
    name = get_doctor_name(d_id)
    notices = get_doctor_notices(d_id)
    return render_template('doctor_dashboard.html', name=name, d_id=d_id, notices=notices)

@app.route('/update_doctor_schedule', methods=['GET', 'POST'], endpoint='update_doctor_schedule')
def update_doctor_schedule_route():
    d_id= session['user_id']
    if 'user_id' not in session:  #######Finally activate this
        flash("Session timed out. Please login again.")
        return redirect(url_for('login'))  # Add your login route
    
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    if request.method == 'POST':
        schedule = {day: request.form.get(day) for day in days}
        telemedicine_day = request.form.get('telemedicine_day')
        update_doctor_schedule(d_id, schedule, telemedicine_day)
        return redirect(url_for('doctor_dashboard'))

    schedule = get_doctor_schedule(d_id)
    return render_template('doctor_schedule.html', doctor=d_id, schedule=schedule or {}, days=days)

#==========added telemed in schedule but couldnt show already selected schedule in frontend

# Helper function to calculate age from DOB
def calculate_age(dob):
    dob = datetime.strptime(str(dob), '%Y-%m-%d')
    today = datetime.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

# @app.route('/doctor_appointments', methods=['GET', 'POST']) ###removed for angshu
# def doctor_appointments():
#     d_id= session['user_id']
#     if 'user_id' not in session:  #######Finally activate this
#         flash("Session timed out. Please login again.")
#         return redirect(url_for('login'))  # Add your login route
    
#     if request.method == 'POST':
#         app_id = request.form.get('app_id')
#         action = request.form.get('action')
        
#         # Update appointment status
#         update_appointment_status(app_id, d_id, action)
#         flash('Updated appointment successfully!', 'success') 
#         return redirect(url_for('doctor_appointments'))

#     # GET - Fetch pending or confirmed + unchecked appointments
#     appointments = get_pending_appointments(d_id)
    
#     # Calculate age for each appointment
#     for appointment in appointments:
#         appointment['age'] = calculate_age(appointment['dob'])

#     return render_template('doctor_appointments.html', appointments=appointments)

#updated doctors's appointment
from models.doctor_model import get_pending_appointments, update_appointment_status 
from models.patient_model import create_notification_for_appointment_action #new line

@app.route('/doctor_appointments', methods=['GET', 'POST'])
def doctor_appointments():
    if 'user_id' not in session:
        flash("Session timed out. Please login again.")
        return redirect(url_for('login'))

    d_id = session['user_id']

    if request.method == 'POST':
        app_id = request.form.get('app_id')
        action = request.form.get('action')

        # Update appointment status first
        update_appointment_status(app_id, d_id, action)

        # Create a notification for the patient based on the action
        create_notification_for_appointment_action(app_id, action) #new line angshu

        flash('Updated appointment successfully!', 'success')
        return redirect(url_for('doctor_appointments'))

    # GET method handling: show pending/confirmed appointments
    appointments = get_pending_appointments(d_id)

    # Calculate age for each appointment
    for appointment in appointments:
        appointment['age'] = calculate_age(appointment['dob'])

    return render_template('doctor_appointments.html', appointments=appointments)


@app.route('/doctor_prescriptions', methods=['GET', 'POST'])
def doctor_prescriptions():
    d_id= session['user_id']
    if 'user_id' not in session:  #######Finally activate this
        flash("Session timed out. Please login again.")
        return redirect(url_for('login'))  # Add your login route

    if request.method == 'POST':
        p_id = request.form['p_id']
        detail = request.form['detail']
        morning = request.form['morning']
        afternoon = request.form['afternoon']
        night = request.form['night']
        date = datetime.today().strftime('%Y-%m-%d')

        if not check_patient_appointment(p_id, d_id):
            flash("This patient doesn't have a confirmed appointment with you.", "warning")
            return redirect(url_for('doctor_prescriptions'))
        
        insert_prescription(p_id, d_id, detail, date, morning, afternoon, night)
        flash('Prescription added successfully!', 'success') 
        return redirect(url_for('doctor_prescriptions'))

    return render_template('doctor_prescriptions.html')


#new code angshu for telemed flow
@app.route('/telemedicine_payment', methods=['GET', 'POST'])
def telemedicine_payment():
    amount = 1000.00  # define this once at the top

    if request.method == 'POST':
        p_id = session['user_id']
        d_id = request.form.get('d_id')
        schedule = request.form.get('schedule')

        # Save payment
        insert_telemedicine_payment(p_id, d_id, schedule, amount)

        # Split schedule
        if " " in schedule:
            date, time = schedule.split(" ", 1)
        else:
            date = schedule
            time = "08:00 - 10:00"

        # Insert appointment
        insert_appointment(d_id, p_id, date, time, 'telemedicine')

        return render_template("make_appointment_process.html", success=True)

    # GET block
    d_id = request.args.get('d_id')
    schedule = request.args.get('schedule')
    return render_template("telemedicine_payment.html", d_id=d_id, schedule=schedule, amount=amount)


def extract_nutrient_percentages(plan):
    nutrients = {
        'Carbohydrates': 0,
        'Proteins': 0,
        'Fats': 0,
        'Vitamins & Minerals': 0
    }
    for line in plan.split('\n'):
        for key in nutrients:
            if key in line:
                match = re.search(r'(\d+)', line)
                if match:
                    nutrients[key] = int(match.group(1))
    return list(nutrients.values())




def calculate_age(dob):
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

@app.route('/diet_suggestion')
def diet_suggestion():
    if 'user_id' not in session:
        flash("Session timed out. Please login again.")
        return redirect(url_for('login'))

    p_id = session['user_id']
    patient = get_patient_details(p_id)

    if not patient:
        return "Patient not found"
    
    #Fetching appointments
    appointments = get_appointment_details(p_id)
    if not appointments:
        return render_template('diet_suggestion.html', message="Diet suggestion will be provided after attending at least one appointment.")

    # Checking if at least one appointment is marked as checked
    has_checked = any(app['checked'] == 1 for app in appointments)

    if not has_checked:
        return render_template('diet_suggestion.html', name=patient['name'], message="Diet suggestion will be provided after attending at least one appointment.")

    age = calculate_age(patient['dob'])
    gender = patient['gender']
    diet_plan = get_diet_plan_by_age_and_gender(age, gender)
    chart_data = extract_nutrient_percentages(diet_plan)
    

    return render_template('diet_suggestion.html', name=patient['name'], age=age, gender=gender, plan=diet_plan, chart_data=chart_data)

#nahian m4
@app.route('/admin_send_notice', methods=['GET', 'POST'])
def admin_send_notice():
    if 'user_id' not in session:
        flash("Session timed out. Please login again.")
        return redirect(url_for('login'))

    admin_id = session['user_id']

    if request.method == 'POST':
        recipient_type = request.form['recipient_type']
        recipient_id = request.form.get('recipient_id')  # Optional
        message = request.form['message']
        date = datetime.today().strftime('%Y-%m-%d')

        if not message:
            flash("Notice message cannot be empty.", "danger")
            return redirect(url_for('admin_send_notice'))

        if recipient_id == '':
            recipient_id = None  # Only needed for specific targets

        insert_notice(admin_id, recipient_type, recipient_id, message, date)
        flash("Notice sent successfully!", "success")
        return redirect(url_for('admin_send_notice'))

    return render_template('admin_send_notice.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
