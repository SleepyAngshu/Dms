########  ADITYA #####################
from db import get_db_connection

def get_medicines_by_pharmacy(pharmacy_id):   ########  ADITYA #####################
    """Get all medicines for a specific pharmacy"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT * FROM medicines 
            WHERE pharmacy_id = %s
            ORDER BY medicine_name
        """, (pharmacy_id,))
        
        medicines = cursor.fetchall()
        
        # Format data for JSON serialization and display
        for medicine in medicines:
            # Format price to 2 decimal places with currency symbol
            if 'price' in medicine and medicine['price'] is not None:
                # Convert to float first to ensure it's a number
                price_value = float(medicine['price'])
                # Format as currency with 2 decimal places
                medicine['price_display'] = f"₹{price_value:.2f}"
                # Keep the original price for calculations
                medicine['price'] = price_value
            
            # Format expiry date
            if 'expiry_date' in medicine and medicine['expiry_date']:
                medicine['expiry_date'] = medicine['expiry_date'].isoformat()
        
        return medicines
    except Exception as e:
        return {'error': str(e)}
    finally:
        cursor.close()
        conn.close()

def add_medicine(data):        ########  ADITYA #####################
    """Add a new medicine"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    result = {'success': False, 'id': None, 'error': None}
    
    try:
        # Check if medicine already exists for this pharmacy
        cursor.execute("""
            SELECT id FROM medicines 
            WHERE pharmacy_id = %s AND medicine_name = %s
        """, (data['pharmacy_id'], data['medicine_name']))
        
        existing = cursor.fetchone()
        
        if existing:
            result['error'] = "This medicine already exists for this pharmacy"
            return result
        
        # Ensure price is stored as a decimal/float
        price = data.get('price')
        if price and isinstance(price, str):
            # Remove currency symbol if present and convert to float
            price = float(price.replace('₹', '').strip())
        
        # Insert new medicine
        cursor.execute("""
            INSERT INTO medicines (pharmacy_id, medicine_name, quantity, price, expiry_date)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            data['pharmacy_id'],
            data['medicine_name'],
            data.get('quantity', 0),
            price,
            data.get('expiry_date')
        ))
        
        conn.commit()
        
        # Get the inserted ID
        result['id'] = cursor.lastrowid
        result['success'] = True
    except Exception as e:
        result['error'] = str(e)
    finally:
        cursor.close()
        conn.close()
    
    return result

def update_medicine(data):       ########  ADITYA #####################
    """Update an existing medicine"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    result = {'success': False, 'error': None}
    
    try:
        # Ensure price is stored as a decimal/float
        price = data.get('price')
        if price and isinstance(price, str):
            # Remove currency symbol if present and convert to float
            price = float(price.replace('₹', '').strip())
        
        # Update medicine
        cursor.execute("""
            UPDATE medicines 
            SET quantity = %s, price = %s, expiry_date = %s
            WHERE id = %s
        """, (
            data.get('quantity', 0),
            price,
            data.get('expiry_date'),
            data['medicine_id']
        ))
        
        conn.commit()
        result['success'] = True
    except Exception as e:
        result['error'] = str(e)
    finally:
        cursor.close()
        conn.close()
    
    return result

def delete_medicine(medicine_id):         ########  ADITYA #####################
    """Delete a medicine"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    result = {'success': False, 'error': None}
    
    try:
        # Delete medicine
        cursor.execute("DELETE FROM medicines WHERE id = %s", (medicine_id,))
        
        conn.commit()
        result['success'] = True
    except Exception as e:
        result['error'] = str(e)
    finally:
        cursor.close()
        conn.close()
    
    return result
