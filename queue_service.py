import uuid
import sqlite3

# DEPRECATED: Old synchronous printer call removed per Day 4 pivot spec
# def print_badge_sync(attendee_id): ...

def publish_print_request(attendee_id):
    """
    Asynchronously publishes a print request payload to the message queue.
    """
    job_id = f"JOB-{uuid.uuid4().hex[:8]}"
    
    conn = sqlite3.connect("kiosk.db")
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE attendees SET status = 'PENDING', print_job_id = ? WHERE attendee_id = ?",
        (job_id, attendee_id)
    )
    conn.commit()
    conn.close()
    
    # Mock message queue payload delivery
    print(f"[QUEUE PRODUCER] Published print request for {attendee_id} with Job ID: {job_id}")
    return job_id