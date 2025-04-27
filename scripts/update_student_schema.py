import sqlite3
from pathlib import Path
import hashlib

def update_student_schema():
    print("Updating student schema to include email and password...")
    
    # Connect to the database
    db_path = Path("data/studipraxis.db")
    if not db_path.exists():
        print("Database file not found!")
        return
    
    # Hash the password "test"
    password_hash = hashlib.sha256("test".encode()).hexdigest()
    
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        # Create new students table with email and password
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students_new (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                year INTEGER NOT NULL,
                interests TEXT NOT NULL,  -- JSON array of strings
                availability TEXT NOT NULL,
                certifications TEXT,      -- JSON array of strings
                created_at TIMESTAMP NOT NULL,
                updated_at TIMESTAMP NOT NULL
            )
        """)
        
        # Get existing students
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        
        # Migrate students to new schema
        for i, student in enumerate(students):
            student_id = student[0]
            name = student[1]
            year = student[2]
            interests = student[3]
            availability = student[4]
            certifications = student[5]
            created_at = student[6]
            updated_at = student[7]
            
            # Create a unique email for each student
            email = f"{name.lower().replace(' ', '_')}_{i}@example.com"
            
            cursor.execute("""
                INSERT INTO students_new (id, name, email, password_hash, year, interests,
                                        availability, certifications, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                student_id,
                name,
                email,
                password_hash,
                year,
                interests,
                availability,
                certifications,
                created_at,
                updated_at
            ))
        
        # Drop old table and rename new one
        cursor.execute("DROP TABLE IF EXISTS students")
        cursor.execute("ALTER TABLE students_new RENAME TO students")
        
        # Get count of updated students
        cursor.execute("SELECT COUNT(*) FROM students")
        count = cursor.fetchone()[0]
        
        conn.commit()
        print(f"Updated schema for {count} students")

if __name__ == "__main__":
    update_student_schema() 