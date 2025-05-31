import random
from datetime import datetime
from pathlib import Path
import sqlite3
import json
import hashlib
from typing import List, Dict, Any
import uuid
import sys
from pathlib import Path

# Add the root directory to the Python path
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from form_options import (
    INTEREST_FIELDS,
    PRAXIS_SKILLS,
    STUDY_YEAR_OPTIONS,
    UNIVERSITY_OPTIONS
)

# Sample hospital data
HOSPITALS = [
    {
        "name": "Universitätsklinikum Hamburg-Eppendorf (UKE)",
        "email": "uke@example.com",
        "location": "Martinistraße 52, 20251 Hamburg",
        "latitude": 53.5897,
        "longitude": 9.9756
    },
    {
        "name": "Asklepios Klinik St. Georg",
        "email": "st.georg@example.com",
        "location": "Lohmühlenstraße 5, 20099 Hamburg",
        "latitude": 53.5553,
        "longitude": 10.0114
    },
    {
        "name": "Asklepios Klinik Barmbek",
        "email": "barmbek@example.com",
        "location": "Rübenkamp 220, 22307 Hamburg",
        "latitude": 53.5869,
        "longitude": 10.0406
    },
    {
        "name": "Marienkrankenhaus Hamburg",
        "email": "marienkrankenhaus@example.com",
        "location": "Alfredstraße 9, 22087 Hamburg",
        "latitude": 53.5678,
        "longitude": 10.0234
    },
    {
        "name": "Albertinen-Krankenhaus",
        "email": "albertinen@example.com",
        "location": "Süntelstraße 11a, 22457 Hamburg",
        "latitude": 53.6234,
        "longitude": 9.8765
    }
]

# Sample position templates for each department
POSITION_TEMPLATES = [
    {
        "department": "Allgemein-/Viszeralchirurgie",
        "title": "Werkstudent in der Allgemein- und Viszeralchirurgie",
        "description": "Mitarbeit bei chirurgischen Eingriffen und der Betreuung von Patient*innen in der Allgemein- und Viszeralchirurgie.",
        "requirements": ["OP-Assistenz", "Lagerung OP", "Patientenaufnahme", "Anamnese"],
        "stipend": "Bezahlung nach Tarifvertrag",
        "min_year": "Klinik - 3. Jahr"
    },
    {
        "department": "Anästhesie",
        "title": "Werkstudent in der Anästhesie",
        "description": "Mitarbeit bei der Vorbereitung und Durchführung von Anästhesien sowie der postoperativen Betreuung.",
        "requirements": ["OP-Assistenz", "Vitalzeichenkontrolle", "Infusionen vorbereiten / anhängen"],
        "stipend": "15",
        "min_year": "Klinik - 4. Jahr"
    },
    {
        "department": "Innere Medizin",
        "title": "Werkstudent in der Inneren Medizin",
        "description": "Mitarbeit bei der Betreuung von internistischen Patient*innen und der Durchführung von Untersuchungen.",
        "requirements": ["Patientenaufnahme", "Anamnese", "Vitalzeichenkontrolle", "Blutentnahme"],
        "stipend": "Bezahlung nach Tarifvertrag",
        "min_year": "Klinik - 3. Jahr"
    },
    {
        "department": "Pädiatrie",
        "title": "Werkstudent in der Pädiatrie",
        "description": "Mitarbeit bei der Betreuung von Kindern und Jugendlichen sowie der Durchführung pädiatrischer Untersuchungen.",
        "requirements": ["Patientenaufnahme", "Anamnese", "Vitalzeichenkontrolle", "Blutentnahme"],
        "stipend": "16",
        "min_year": "Klinik - 4. Jahr"
    },
    {
        "department": "Notfallmedizin",
        "title": "Werkstudent in der Notaufnahme",
        "description": "Mitarbeit in der Notaufnahme bei der Ersteinschätzung und Betreuung von Notfallpatient*innen.",
        "requirements": ["Ersteinschätzung (ZNA / Triage)", "Vitalzeichenkontrolle", "Blutentnahme", "Infusionen vorbereiten / anhängen"],
        "stipend": "Bezahlung nach Tarifvertrag",
        "min_year": "Klinik - 4. Jahr"
    }
]

# Sample student names
STUDENT_NAMES = [
    "Anna Müller", "Luca Ferrari", "Maya Patel", "Jonas Schmidt", "Sophie Weber",
    "Maximilian Becker", "Emma Fischer", "Leon Wagner", "Lina Hoffmann", "Felix Bauer",
    "Hannah Wolf", "Tim Schneider", "Laura Meyer", "Paul Fischer", "Julia Wagner",
    "David Becker", "Sarah Hoffmann", "Niklas Wolf", "Marie Schmidt", "Jan Fischer"
]

def generate_student_data() -> List[Dict[str, Any]]:
    """Generate sample student data."""
    students = []
    for name in STUDENT_NAMES:
        # Generate random year from STUDY_YEAR_OPTIONS
        year = random.choice(STUDY_YEAR_OPTIONS)
        
        # Generate random interests (2-4)
        num_interests = random.randint(2, 4)
        interests = random.sample(INTEREST_FIELDS, num_interests)
        
        # Generate random certifications (0-3)
        num_certs = random.randint(0, 3)
        certifications = random.sample(PRAXIS_SKILLS, num_certs) if num_certs > 0 else None
        
        # Generate praxiserfahrungen
        praxiserfahrungen = f"Famulatur in {random.choice(['Chirurgie', 'Innere Medizin', 'Pädiatrie', 'Gynäkologie'])}"
        
        students.append({
            "name": name,
            "email": f"{name.lower().replace(' ', '_')}@example.com",
            "year": year,
            "interests": interests,
            "praxiserfahrungen": praxiserfahrungen,
            "certifications": certifications
        })
    
    return students

def generate_positions_for_hospital(hospital_id: str) -> List[Dict[str, Any]]:
    """Generate sample positions for a hospital."""
    positions = []
    # Each hospital gets 3-5 random positions
    num_positions = random.randint(3, 5)
    selected_templates = random.sample(POSITION_TEMPLATES, num_positions)
    
    for template in selected_templates:
        position = template.copy()
        position["hospital_id"] = hospital_id
        positions.append(position)
    
    return positions

def main():
    print("Starting fresh data generation...")
    
    # Connect to the database
    db_path = Path("data/studipraxis.db")
    if not db_path.exists():
        print("Database file not found!")
        return
    
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        # Clear existing data
        cursor.execute("DELETE FROM matches")
        cursor.execute("DELETE FROM positions")
        cursor.execute("DELETE FROM hospitals")
        cursor.execute("DELETE FROM students")
        
        # Hash the password "test"
        password_hash = hashlib.sha256("test".encode()).hexdigest()
        
        # Insert hospitals
        for hospital in HOSPITALS:
            hospital_id = str(uuid.uuid4())
            now = datetime.now().isoformat()
            
            cursor.execute("""
                INSERT INTO hospitals (id, name, email, password_hash, location, 
                                     latitude, longitude, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                hospital_id,
                hospital["name"],
                hospital["email"],
                password_hash,
                hospital["location"],
                hospital["latitude"],
                hospital["longitude"],
                now,
                now
            ))
            
            # Generate positions for this hospital
            positions = generate_positions_for_hospital(hospital_id)
            for position in positions:
                position_id = str(uuid.uuid4())
                cursor.execute("""
                    INSERT INTO positions (id, hospital_id, department, title, description,
                                         requirements, min_year, stipend, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    position_id,
                    position["hospital_id"],
                    position["department"],
                    position["title"],
                    position["description"],
                    json.dumps(position["requirements"]),
                    position["min_year"],
                    position["stipend"],
                    now,
                    now
                ))
        
        # Insert students
        students = generate_student_data()
        for student in students:
            student_id = str(uuid.uuid4())
            now = datetime.now().isoformat()
            
            cursor.execute("""
                INSERT INTO students (id, name, email, password_hash, year, interests,
                                    praxiserfahrungen, certifications, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                student_id,
                student["name"],
                student["email"],
                password_hash,
                student["year"],
                json.dumps(student["interests"]),
                student["praxiserfahrungen"],
                json.dumps(student["certifications"]) if student["certifications"] else None,
                now,
                now
            ))
        
        conn.commit()
        print("Fresh data generation completed successfully!")

if __name__ == "__main__":
    main() 