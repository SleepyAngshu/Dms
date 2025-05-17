from db import get_db_connection

def get_all_pharmacies():           #######  ADITYA ########
    """Get all pharmacies"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM pharmacies")
        rows = cursor.fetchall()
        
        # Convert MySQL cursor results to a list of dictionaries
        pharmacies = []
        for row in rows:
            pharmacy = dict(row)
            # Ensure numeric values are properly formatted
            pharmacy['longitude'] = float(pharmacy['longitude']) if pharmacy['longitude'] else None
            pharmacy['latitude'] = float(pharmacy['latitude']) if pharmacy['latitude'] else None
            
            pharmacies.append(pharmacy)
        
        return pharmacies
    finally:
        cursor.close()
        conn.close()

def get_nearby_pharmacies(lat, lng, radius=5):           #######  ADITYA ########
    """Get pharmacies within a certain radius using Haversine formula"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Using the Haversine formula in SQL to calculate distance
        query = """
        SELECT 
            *,
            (
                6371 * acos(
                    cos(radians(%s)) * 
                    cos(radians(latitude)) * 
                    cos(radians(longitude) - radians(%s)) + 
                    sin(radians(%s)) * 
                    sin(radians(latitude))
                )
            ) AS distance
        FROM 
            pharmacies
        HAVING 
            distance < %s
        ORDER BY 
            distance
        """
        
        cursor.execute(query, (lat, lng, lat, radius))
        
        # Convert MySQL cursor results to a list of dictionaries
        pharmacies = []
        for row in cursor.fetchall():
            pharmacy = dict(row)
            # Ensure numeric values are properly formatted
            pharmacy['longitude'] = float(pharmacy['longitude']) if pharmacy['longitude'] else None
            pharmacy['latitude'] = float(pharmacy['latitude']) if pharmacy['latitude'] else None
            
            pharmacy['distance'] = float(pharmacy['distance']) if 'distance' in pharmacy else None
            pharmacies.append(pharmacy)
        
        return pharmacies
    finally:
        cursor.close()
        conn.close()
