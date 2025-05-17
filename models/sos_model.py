from db import get_db_connection

def get_all_sos_alerts():          #######  ANGSHU########
    """Get all SOS alerts"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM sos_alerts ORDER BY timestamp DESC")
        sos_alerts = cursor.fetchall()
        return sos_alerts
    finally:
        cursor.close()
        conn.close()


def update_sos_alert_status(alert_id, responded=1):      #######  ANGSHU########
    """Update the responded status of an SOS alert"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE sos_alerts SET responded = %s WHERE p_id = %s",
            (responded, alert_id)
        )
        conn.commit()
        success = cursor.rowcount > 0  # Returns True if at least one row was updated
        return success
    except Exception as e:
        conn.rollback()
        print(f"Database error in update_sos_alert_status: {str(e)}")
        raise e
    finally:
        cursor.close()
        conn.close()
