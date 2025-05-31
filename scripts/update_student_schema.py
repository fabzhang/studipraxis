import sqlite3
from pathlib import Path
import hashlib
from datetime import datetime

def update_student_schema():
    print("Updating student schema to rename availability to praxiserfahrungen...")
    
    # Connect to the database
    db_path = Path("data/studipraxis.db")
    if not db_path.exists():
        print("Database file not found!")
        return
    
    # Hash the password "test"
    password_hash = hashlib.sha256("test".encode()).hexdigest()
    
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        # Create new students table with renamed column
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students_new (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                year INTEGER NOT NULL,
                interests TEXT NOT NULL,  -- JSON array of strings
                praxiserfahrungen TEXT NOT NULL,
                certifications TEXT,      -- JSON array of strings
                created_at TIMESTAMP NOT NULL,
                updated_at TIMESTAMP NOT NULL
            )
        """)
        
        # Get existing students
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        
        # Get current timestamp
        now = datetime.now().isoformat()
        
        # Migrate students to new schema
        for i, student in enumerate(students):
            student_id = student[0]
            name = student[1]
            email = student[2]
            password_hash = student[3]
            year = student[4]
            interests = student[5]
            availability = student[6]  # This will be migrated to praxiserfahrungen
            certifications = student[7]
            created_at = student[8] if student[8] else now
            updated_at = student[9] if student[9] else now
            
            # Create a unique email for each student
            email = f"{name.lower().replace(' ', '_')}_{i}@example.com"
            
            cursor.execute("""
                INSERT INTO students_new (id, name, email, password_hash, year, interests,
                                        praxiserfahrungen, certifications, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                student_id,
                name,
                email,
                password_hash,
                year,
                interests,
                availability,  # Migrate availability to praxiserfahrungen
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