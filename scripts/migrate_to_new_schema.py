import sqlite3
from pathlib import Path
from datetime import datetime
import json
import uuid

def migrate_to_new_schema():
    print("Starting migration to new schema...")
    
    # Connect to the database
    db_path = Path("data/studipraxis.db")
    if not db_path.exists():
        print("Database file not found!")
        return
    
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        # Create new tables
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS hospitals_new (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                location TEXT NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                created_at TIMESTAMP NOT NULL,
                updated_at TIMESTAMP NOT NULL
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS positions_new (
                id TEXT PRIMARY KEY,
                hospital_id TEXT NOT NULL,
                department TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                duration TEXT NOT NULL,
                requirements TEXT NOT NULL,
                stipend REAL,
                created_at TIMESTAMP NOT NULL,
                updated_at TIMESTAMP NOT NULL,
                FOREIGN KEY (hospital_id) REFERENCES hospitals_new(id)
            )
        """)
        
        # Get existing hospitals
        cursor.execute("SELECT * FROM hospitals")
        hospitals = cursor.fetchall()
        
        # Migrate hospitals to new schema
        for i, hospital in enumerate(hospitals):
            hospital_id = hospital[0]
            name = hospital[1]
            location = hospital[7]
            latitude = hospital[8]
            longitude = hospital[9]
            created_at = hospital[11]
            updated_at = hospital[12]
            
            # Create a unique email for each hospital
            email = f"{name.lower().replace(' ', '_')}_{i}@example.com"
            password_hash = "dummy_hash"  # You'll need to set real passwords later
            
            cursor.execute("""
                INSERT INTO hospitals_new (id, name, email, password_hash, location,
                                         latitude, longitude, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                hospital_id,
                name,
                email,
                password_hash,
                location,
                latitude,
                longitude,
                created_at,
                updated_at
            ))
            
            # Migrate positions
            cursor.execute("""
                INSERT INTO positions_new (id, hospital_id, department, title, description,
                                         duration, requirements, stipend, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                str(uuid.uuid4()),
                hospital_id,
                hospital[2],  # department
                hospital[3],  # title
                hospital[4],  # description
                hospital[5],  # duration
                hospital[6],  # requirements
                hospital[10], # stipend
                created_at,
                updated_at
            ))
        
        # Drop old tables and rename new ones
        cursor.execute("DROP TABLE IF EXISTS hospitals")
        cursor.execute("DROP TABLE IF EXISTS positions")
        cursor.execute("ALTER TABLE hospitals_new RENAME TO hospitals")
        cursor.execute("ALTER TABLE positions_new RENAME TO positions")
        
        conn.commit()
        print("Migration completed successfully!")

if __name__ == "__main__":
    migrate_to_new_schema() 