import sqlite3

def init_db():
    conn = sqlite3.connect("kiosk.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendees (
            attendee_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'UNCHECKED',
            print_job_id TEXT
        )
    """)
    # Seed test data
    cursor.executemany("""
        INSERT OR IGNORE INTO attendees (attendee_id, name, status) 
        VALUES (?, ?, 'UNCHECKED')
    """, [("ATT-001", "Alice"), ("ATT-002", "Bob"), ("ATT-003", "Charlie")])
    conn.commit()
    conn.close()

def get_attendee(attendee_id):
    conn = sqlite3.connect("kiosk.db")
    cursor = conn.cursor()
    cursor.execute("SELECT attendee_id, name, status, print_job_id FROM attendees WHERE attendee_id = ?", (attendee_id,))
    row = cursor.fetchone()
    conn.close()
    return row