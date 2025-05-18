# models/doctor_model.py
from db import get_db_connection

def get_doctor_by_id(d_id):           ###########  AFIA ##############
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM doctor WHERE d_id = %s", (d_id,))
    doctor = cursor.fetchone()
    cursor.close()
    conn.close()
    return doctor

def update_doctor_profile(d_id, designation, phone, location):    ########## NAHIAN #############
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE doctor SET designation = %s, phone = %s, location = %s
        WHERE d_id = %s
    """, (designation, phone, location, d_id))
    conn.commit()
    cursor.close()
    conn.close()

def get_doctor_name(d_id):           ######### NAHIAN ############
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT name FROM doctor WHERE d_id = %s", (d_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result['name'] if result else None


def get_doctor_schedule(d_id):       ######### NAHIAN ############
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM doctor_schedule WHERE d_id = %s", (d_id,))
    schedule = cursor.fetchone()
    cursor.close()
    conn.close()
    return schedule

def update_doctor_schedule(d_id, schedule, telemedicine_days):  ######### NAHIAN ############
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        REPLACE INTO doctor_schedule 
        (d_id, monday, tuesday, wednesday, thursday, friday, saturday, sunday, telemedicine_days)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (d_id, schedule['Monday'], schedule['Tuesday'], schedule['Wednesday'],
          schedule['Thursday'], schedule['Friday'], schedule['Saturday'], schedule['Sunday'], telemedicine_days))


    conn.commit()
    cursor.close()
    conn.close()

def get_pending_appointments(d_id):         ######### NAHIAN ############
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = '''
        SELECT appointment.*, patient.name, patient.phone, patient.weight, patient.gender, patient.dob,
               patient.gl_b_breakfast, patient.gl_a_breakfast, patient.gl_b_lunch, patient.gl_b_dinner
        FROM appointment
        JOIN patient ON appointment.p_id = patient.p_id
        WHERE appointment.d_id = %s AND (appointment.confirmation = 0 OR appointment.confirmation = 1) 
              AND appointment.checked = 0
    '''
    cursor.execute(query, (d_id,))
    appointments = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return appointments

def update_appointment_status(app_id, d_id, action):       ######### NAHIAN ############
    conn = get_db_connection()
    cursor = conn.cursor()
    action_map = {
        'Confirm': 1,
        'Cancel': 2,
        'Reschedule': 3
    }
    
    if action == 'Checked':
        cursor.execute("UPDATE appointment SET checked = 1 WHERE app_id = %s AND d_id = %s", (app_id, d_id))
    elif action in action_map:
        cursor.execute("UPDATE appointment SET confirmation = %s WHERE app_id = %s AND d_id = %s",
                       (action_map[action], app_id, d_id))

    conn.commit()
    cursor.close()
    conn.close()


def insert_prescription(p_id, d_id, detail, date, morning, afternoon, night):  ######### NAHIAN ############
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO prescription (p_id, d_id, detail, date, morning, afternoon, night)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (p_id, d_id, detail, date, morning, afternoon, night))
    conn.commit()
    cursor.close()
    conn.close()


def check_patient_appointment(p_id, d_id):      ######### NAHIAN ############
    conn = get_db_connection()
    cursor = conn.cursor(buffered=True)
    query = """
        SELECT 1 FROM appointment
        WHERE p_id = %s AND d_id = %s AND confirmation = 1
    """
    cursor.execute(query, (p_id, d_id))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None

#nahian m4
def get_doctor_notices(d_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT * FROM notices
        WHERE 
            recipient_type = 'doctor'
            OR recipient_type = 'both'
            OR (recipient_type = 'specific_doctor' AND recipient_id = %s)
        ORDER BY date DESC
    """
    cursor.execute(query, (d_id,))
    results = cursor.fetchall()

    cursor.close()
    connection.close()
    return results
