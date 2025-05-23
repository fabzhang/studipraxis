import json
from pathlib import Path
from datetime import datetime
from backend.services.database import DatabaseService
from shared.types import StudentProfile, HospitalProfile

def migrate_data():
    print("Starting migration to SQLite database...")
    db_service = DatabaseService()
    
    # Migrate students
    students_file = Path("data/students/students.json")
    if students_file.exists() and students_file.stat().st_size > 0:
        print("Migrating students...")
        with open(students_file) as f:
            students_data = json.load(f)
            
        for student_data in students_data:
            # Convert string year to integer
            year = int(student_data.get("year", "1"))
            
            # Convert interests and certifications to lists
            interests = [i.strip() for i in student_data.get("interests", "").split(",") if i.strip()]
            certifications = [c.strip() for c in student_data.get("certifications", "").split(",") if c.strip()]
            
            student = StudentProfile(
                id="",  # Will be generated by service
                name=student_data.get("name", ""),
                year=year,
                interests=interests,
                availability=student_data.get("availability", ""),
                certifications=certifications if certifications else None,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            db_service.create_student(student)
            print(f"Migrated student: {student.name}")
    else:
        print("No students data to migrate.")
    
    # Migrate hospitals
    hospitals_file = Path("data/hospitals/hospitals.json")
    if hospitals_file.exists() and hospitals_file.stat().st_size > 0:
        print("Migrating hospitals...")
        with open(hospitals_file) as f:
            hospitals_data = json.load(f)
            
        for hospital_data in hospitals_data:
            # Convert requirements to list if it's a string
            requirements = hospital_data.get("requirements", [])
            if isinstance(requirements, str):
                requirements = [r.strip() for r in requirements.split(",") if r.strip()]
            
            hospital = HospitalProfile(
                id="",  # Will be generated by service
                name=hospital_data.get("name", ""),
                department=hospital_data.get("department", ""),
                title=hospital_data.get("title", ""),
                description=hospital_data.get("description", ""),
                duration=hospital_data.get("duration", ""),
                requirements=requirements,
                location=hospital_data.get("location", ""),
                latitude=hospital_data.get("latitude", 0.0),
                longitude=hospital_data.get("longitude", 0.0),
                stipend=hospital_data.get("stipend"),
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            db_service.create_hospital(hospital)
            print(f"Migrated hospital: {hospital.name}")
    else:
        print("No hospitals data to migrate.")
    
    print("Migration completed successfully!")

if __name__ == "__main__":
    migrate_data() 