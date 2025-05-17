from db import get_db_connection
from datetime import datetime



def search_medicines_by_name(search_term):      ########  ADITYA #####################

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        
        
        cursor.execute("""
            SELECT id, medicine_name, price, quantity 
            FROM medicines 
            WHERE medicine_name LIKE %s
            LIMIT 10
        """, (f'%{search_term}%',))
        
        medicines = cursor.fetchall()
        
        # Format data for JSON serialization and display
        for medicine in medicines:
            # Format price to 2 decimal places with currency symbol
            if 'price' in medicine and medicine['price'] is not None:
                # Convert to float first to ensure it's a number
                price_value = float(medicine['price'])
                # Format as currency with 2 decimal places
                medicine['price_display'] = f"৳{price_value:.2f}"
                # Keep the original price for calculations
                medicine['price'] = price_value
            
            
        
        return medicines
    except Exception as e:
        print(f"Error searching medicines: {e}")
        return []
    finally:
        cursor.close()
        conn.close()
    

def create_order(p_id, items, delivery_address, data={}):         ########  ADITYA #####################

    conn = get_db_connection()
    cursor = conn.cursor()
    try:

        # Get payment method from data or default to cash
        payment_method = data.get('payment_method', 'cash')

        # Insert order
        order_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("""
            INSERT INTO orders (p_id,order_date,status,delivery_address,payment_method)
            VALUES ( %s, %s, %s, %s, %s)
        """, ( p_id, order_date, 'pending', delivery_address,payment_method))
        
        order_id = cursor.lastrowid
        
        # Insert order items
        for item in items:
            cursor.execute("""
                INSERT INTO order_items (order_id, medicine_name, quantity, price)
                VALUES (%s, %s, %s, %s)
            """, (order_id, item['medicine_name'], item['quantity'], item['price']))
        
        # Commit transaction
        conn.commit()
        return {"success": True, "order_id": order_id}
    except Exception as e:
        # Rollback in case of error
        conn.rollback()
        return {"success": False, "error": str(e)}
    finally:
        cursor.close()
        conn.close()

def get_patient_orders(p_id):           ########  ADITYA #####################
    """Get all orders for a patient"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Check if orders table exists
        cursor.execute("SHOW TABLES LIKE 'orders'")
        if not cursor.fetchone():
            return []
        
        query = """
            SELECT o.*
            FROM orders o           
            ORDER BY o.order_date DESC
        """
        cursor.execute(query, (p_id,))
        orders = cursor.fetchall()
        
        # Get items for each order
        for order in orders:
            query = """
                SELECT oi.*, m.medicine_name
                FROM order_items oi
                JOIN medicines m ON oi.medicine_id = m.id
                WHERE oi.order_id = %s
            """
            cursor.execute(query, (order['order_id'],))
            order['items'] = cursor.fetchall()
            
            # Calculate total
            order['total'] = sum(float(item['price']) * item['quantity'] for item in order['items'])
            
        return orders
    except Exception as e:
        print(f"Error getting patient orders: {e}")
        return []
    finally:
        cursor.close()
        conn.close()




