import json
from typing import List, Optional
from datetime import datetime
import uuid
from pathlib import Path

from shared.types import StudentProfile, HospitalProfile, Message, Match

class DataService:
    def __init__(self):
        self.students_file = Path("data/students/students.json")
        self.hospitals_file = Path("data/hospitals/hospitals.json")
        self.messages_file = Path("data/messages.json")
        self.matches_file = Path("data/matches.json")
        
        # Ensure data directories exist
        self.students_file.parent.mkdir(parents=True, exist_ok=True)
        self.hospitals_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize files if they don't exist
        if not self.students_file.exists():
            self.students_file.write_text("[]")
        if not self.hospitals_file.exists():
            self.hospitals_file.write_text("[]")
        if not self.messages_file.exists():
            self.messages_file.write_text("[]")
        if not self.matches_file.exists():
            self.matches_file.write_text("[]")

    def _load_json(self, file_path: Path) -> List[dict]:
        return json.loads(file_path.read_text())

    def _save_json(self, file_path: Path, data: List[dict]):
        file_path.write_text(json.dumps(data, indent=2))

    # Student operations
    def create_student(self, student: StudentProfile) -> StudentProfile:
        students = self._load_json(self.students_file)
        student_dict = {
            "id": str(uuid.uuid4()),
            "name": student.name,
            "year": student.year,
            "interests": student.interests,
            "availability": student.availability,
            "certifications": student.certifications,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        students.append(student_dict)
        self._save_json(self.students_file, students)
        return StudentProfile(**student_dict)

    def get_students(self) -> List[StudentProfile]:
        students = self._load_json(self.students_file)
        return [StudentProfile(**student) for student in students]

    # Hospital operations
    def create_hospital(self, hospital: HospitalProfile) -> HospitalProfile:
        hospitals = self._load_json(self.hospitals_file)
        hospital_dict = {
            "id": str(uuid.uuid4()),
            "name": hospital.name,
            "department": hospital.department,
            "title": hospital.title,
            "description": hospital.description,
            "duration": hospital.duration,
            "requirements": hospital.requirements,
            "location": hospital.location,
            "latitude": hospital.latitude,
            "longitude": hospital.longitude,
            "stipend": hospital.stipend,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        hospitals.append(hospital_dict)
        self._save_json(self.hospitals_file, hospitals)
        return HospitalProfile(**hospital_dict)

    def get_hospitals(self) -> List[HospitalProfile]:
        hospitals = self._load_json(self.hospitals_file)
        return [HospitalProfile(**hospital) for hospital in hospitals]

    # Message operations
    def create_message(self, message: Message) -> Message:
        messages = self._load_json(self.messages_file)
        message_dict = {
            "id": str(uuid.uuid4()),
            "sender_id": message.sender_id,
            "receiver_id": message.receiver_id,
            "content": message.content,
            "created_at": datetime.now().isoformat(),
            "read": False
        }
        messages.append(message_dict)
        self._save_json(self.messages_file, messages)
        return Message(**message_dict)

    def get_messages(self, user_id: str) -> List[Message]:
        messages = self._load_json(self.messages_file)
        return [Message(**msg) for msg in messages 
                if msg["sender_id"] == user_id or msg["receiver_id"] == user_id]

    # Match operations
    def create_match(self, match: Match) -> Match:
        matches = self._load_json(self.matches_file)
        match_dict = {
            "id": str(uuid.uuid4()),
            "student_id": match.student_id,
            "hospital_id": match.hospital_id,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        matches.append(match_dict)
        self._save_json(self.matches_file, matches)
        return Match(**match_dict)

    def get_matches(self, user_id: str) -> List[Match]:
        matches = self._load_json(self.matches_file)
        return [Match(**match) for match in matches 
                if match["student_id"] == user_id or match["hospital_id"] == user_id] 