from typing import List, Optional
from datetime import datetime
import uuid

from shared.types import StudentProfile, HospitalProfile, Message, Match, Position
from backend.services.database import DatabaseService

class DataService:
    def __init__(self):
        self.db_service = DatabaseService()

    # Student operations
    def create_student(self, student: StudentProfile) -> StudentProfile:
        return self.db_service.create_student(student)

    def get_students(self) -> List[StudentProfile]:
        return self.db_service.get_students()

    def get_student(self, student_id: str) -> Optional[StudentProfile]:
        return self.db_service.get_student(student_id)

    def authenticate_student(self, email: str, password: str) -> Optional[StudentProfile]:
        return self.db_service.authenticate_student(email, password)

    def create_student_account(self, name: str, email: str, password: str, year: int, 
                             interests: List[str], availability: str, 
                             certifications: Optional[List[str]] = None) -> StudentProfile:
        return self.db_service.create_student_account(
            name, email, password, year, interests, availability, certifications
        )

    # Hospital account operations
    def create_hospital_account(self, name: str, email: str, password: str, location: str, latitude: float, longitude: float) -> HospitalProfile:
        return self.db_service.create_hospital_account(name, email, password, location, latitude, longitude)

    def authenticate_hospital(self, email: str, password: str) -> Optional[HospitalProfile]:
        return self.db_service.authenticate_hospital(email, password)

    def get_hospital(self, hospital_id: str) -> Optional[HospitalProfile]:
        return self.db_service.get_hospital(hospital_id)

    def get_hospitals(self) -> List[HospitalProfile]:
        return self.db_service.get_hospitals()

    # Position operations
    def create_position(self, position: Position) -> Position:
        return self.db_service.create_position(position)

    def get_positions(self, hospital_id: Optional[str] = None) -> List[Position]:
        return self.db_service.get_positions(hospital_id)

    def get_position(self, position_id: str) -> Optional[Position]:
        return self.db_service.get_position(position_id)

    # Message operations
    def create_message(self, message: Message) -> Message:
        return self.db_service.create_message(message)

    def get_messages(self, user_id: str) -> List[Message]:
        return self.db_service.get_messages(user_id)

    # Match operations
    def create_match(self, match: Match) -> Match:
        return self.db_service.create_match(match)

    def get_matches(self, user_id: str) -> List[Match]:
        return self.db_service.get_matches(user_id)

    def get_match_by_student_and_position(self, student_id: str, position_id: str) -> Optional[Match]:
        return self.db_service.get_match_by_student_and_position(student_id, position_id)

    def update_match_status(self, match_id: str, status: str) -> Match:
        return self.db_service.update_match_status(match_id, status)

    def get_applications_for_position(self, position_id: str) -> List[Match]:
        return self.db_service.get_applications_for_position(position_id)

    def get_saved_positions_for_student(self, student_id: str) -> List[Match]:
        return self.db_service.get_saved_positions_for_student(student_id)

    def get_applied_positions_for_student(self, student_id: str) -> List[Match]:
        return self.db_service.get_applied_positions_for_student(student_id) 