import sqlite3
from pathlib import Path
import hashlib

def update_passwords():
    print("Updating hospital passwords to 'test'...")
    
    # Connect to the database
    db_path = Path("data/studipraxis.db")
    if not db_path.exists():
        print("Database file not found!")
        return
    
    # Hash the password "test"
    password_hash = hashlib.sha256("test".encode()).hexdigest()
    
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        # Update all hospital passwords
        cursor.execute("""
            UPDATE hospitals
            SET password_hash = ?
        """, (password_hash,))
        
        # Get count of updated hospitals
        cursor.execute("SELECT COUNT(*) FROM hospitals")
        count = cursor.fetchone()[0]
        
        conn.commit()
        print(f"Updated passwords for {count} hospitals to 'test'")

if __name__ == "__main__":
    update_passwords() 