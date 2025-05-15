#from utils.db import get_connection
from db import get_db_connection

def get_all_appointments():
    """Get all appointments with doctor and patient names"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT a.*, d.name as doctor_name, p.name as patient_name 
            FROM appointment a
            JOIN doctor d ON a.d_id = d.d_id
            JOIN patient p ON a.p_id = p.p_id
            ORDER BY a.date DESC, a.time DESC
        """)
        appointments = cursor.fetchall()
        return appointments
    finally:
        cursor.close()
        conn.close()

# def update_appointment_status(app_id, action):
#     """Update appointment status"""
#     conn = get_db_connection()
#     cursor = conn.cursor(dictionary=True)
#     result = {'success': False, 'message': ''}
    
#     try:
#         if action == 'Confirm':
#             cursor.execute("UPDATE appointment SET confirmation = 1 WHERE app_id = %s", (app_id,))
#             result['message'] = f'Appointment ID {app_id} has been confirmed!'
#         elif action == 'Cancel':
#             cursor.execute("UPDATE appointment SET confirmation = 2 WHERE app_id = %s", (app_id,))
#             result['message'] = f'Appointment ID {app_id} has been cancelled.'
#         elif action == 'Mark Checked':
#             cursor.execute("UPDATE appointment SET checked = 1 WHERE app_id = %s", (app_id,))
#             result['message'] = f'Appointment ID {app_id} has been marked as checked.'
            
#         conn.commit()
#         result['success'] = True
#     except Exception as e:
#         result['message'] = f'Error: {str(e)}'
#     finally:
#         cursor.close()
#         conn.close()
    
#     return result

def get_all_prescriptions():
    """Get all prescriptions with doctor and patient names"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT p.*, d.name as doctor_name, pt.name as patient_name 
            FROM prescription p
            JOIN doctor d ON p.d_id = d.d_id
            JOIN patient pt ON p.p_id = pt.p_id
            ORDER BY p.date DESC
        """)
        prescriptions = cursor.fetchall()
        return prescriptions
    finally:
        cursor.close()
        conn.close()

#new code angshu

def insert_telemedicine_payment(p_id, d_id, schedule, amount):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        INSERT INTO telemedicine_payment (p_id, d_id, schedule, amount)
        VALUES (%s, %s, %s, %s)
    """, (p_id, d_id, schedule, amount))
    conn.commit()
    cursor.close()
    conn.close()