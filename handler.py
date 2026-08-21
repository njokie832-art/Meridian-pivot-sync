import json
import sqlite3
from db_state import get_attendee
from queue_service import publish_print_request

def check_in_scan_handler(event, context):
    """
    Triggered when an attendee QR code is scanned at the kiosk.
    """
    body = json.loads(event.get("body", "{}"))
    attendee_id = body.get("attendee_id")
    
    attendee = get_attendee(attendee_id)
    if not attendee:
        return {"statusCode": 404, "body": json.dumps({"error": "Attendee not found"})}
    
    _, name, status, _ = attendee
    
    # Idempotency guard: duplicate scan check
    if status in ["PENDING", "CHECKED_IN"]:
        return {
            "statusCode": 409,
            "body": json.dumps({
                "message": f"Duplicate scan rejected. Attendee is already in state: {status}",
                "status": status
            })
        }
    
    # Transition state to PENDING and trigger queue message
    job_id = publish_print_request(attendee_id)
    
    return {
        "statusCode": 202,
        "body": json.dumps({
            "message": "Check-in initiated. Badge printing pending.",
            "attendee_id": attendee_id,
            "status": "PENDING",
            "job_id": job_id
        })
    }

def printer_webhook_handler(event, context):
    """
    Webhook callback endpoint invoked asynchronously by the vendor printer service.
    """
    body = json.loads(event.get("body", "{}"))
    job_id = body.get("job_id")
    print_status = body.get("status") # e.g., "COMPLETED"
    
    if print_status != "COMPLETED":
        return {"statusCode": 400, "body": json.dumps({"error": "Print job failed or incomplete"})}
    
    conn = sqlite3.connect("kiosk.db")
    cursor = conn.cursor()
    cursor.execute("SELECT attendee_id, status FROM attendees WHERE print_job_id = ?", (job_id,))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        return {"statusCode": 404, "body": json.dumps({"error": "Job ID not found"})}
    
    attendee_id, current_status = row
    
    # Ensure idempotency for duplicate or out-of-order webhook callbacks
    if current_status == "CHECKED_IN":
        conn.close()
        return {"statusCode": 200, "body": json.dumps({"message": "Already marked as CHECKED_IN"})}
    
    cursor.execute("UPDATE attendees SET status = 'CHECKED_IN' WHERE print_job_id = ?", (job_id,))
    conn.commit()
    conn.close()
    
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Badge print confirmed. Attendee checked in successfully.",
            "attendee_id": attendee_id,
            "status": "CHECKED_IN"
        })
    }