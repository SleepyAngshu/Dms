#############   AFIA,NAIHAN,ANGSHU,ADITYA ##############
from db import get_db_connection
import re
from datetime import datetime

def validate_email(email):
    """Validate email format"""
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_pattern, email)

def login_user(email, password, role):
    """Login a user based on role"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    # conn, cursor = get_db_connection()
    user = None
    
    try:
        if role == 'admin':
            cursor.execute('SELECT * FROM admin WHERE email = %s AND password = %s', (email, password))
            user = cursor.fetchone()
            if user:
                user_data = {
                    'user_id': user['id'],
                    'email': user['email'],
                    'role': 'admin',
                    'name': user.get('name', 'Admin')
                }
        elif role == 'doctor':
            cursor.execute('SELECT * FROM doctor WHERE email = %s AND password = %s', (email, password))
            user = cursor.fetchone()
            if user:
                user_data = {
                    'user_id': user['d_id'],
                    'email': user['email'],
                    'role': 'doctor',
                    'name': user['name']
                }
        elif role == 'patient':
            cursor.execute('SELECT * FROM patient WHERE email = %s AND password = %s', (email, password))
            user = cursor.fetchone()
            if user:
                user_data = {
                    'user_id': user['p_id'],
                    'email': user['email'],
                    'role': 'patient',
                    'name': user['name']
                }
    finally:
        cursor.close()
        conn.close()
    
    return user_data if user else None
    

def register_user(username, email, password, role):
    print("MEthod in")
    """Register a new user"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    # conn, cursor = get_db_connection()
    result = {'success': False, 'message': ''}
    
    try:
        # Check if email already exists in the appropriate table
        if role == 'Doctor':
            cursor.execute('SELECT * FROM doctor WHERE email = %s', (email,))
            if cursor.fetchone():
                result['message'] = 'Email already registered as a doctor'
                return result
            
            # Insert new doctor
            current_date = datetime.now().strftime('%Y-%m-%d')
            cursor.execute(
                'INSERT INTO doctor (name, email, password, designation, verified) VALUES (%s, %s, %s, %s, %s)',
                (username, email, password, 'General Physician', 0)
            )
            conn.commit()
            result['success'] = True
            result['message'] = 'Registration successful! Please wait for admin verification before logging in.'
            
        elif role == 'Patient':
            cursor.execute('SELECT * FROM patient WHERE email = %s', (email,))
            if cursor.fetchone():
                result['message'] = 'Email already registered as a patient'
                return result
            
            # Insert new patient
            current_date = datetime.now().strftime('%Y-%m-%d')
            cursor.execute(
                'INSERT INTO patient (name, email, password) VALUES (%s, %s, %s)',
                (username, email, password)
            )
            conn.commit()
            result['success'] = True
            result['message'] = 'Registration successful! You can now login.'
    except Exception as e:
        result['message'] = f'Database error: {str(e)}'
    finally:
        cursor.close()
        conn.close()
    
    return result
