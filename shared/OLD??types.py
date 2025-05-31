from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class StudentProfile:
    id: str
    name: str
    email: str
    password_hash: str
    year: int
    interests: List[str]
    praxiserfahrungen: str
    certifications: Optional[List[str]]
    created_at: datetime
    updated_at: datetime

@dataclass
class HospitalProfile:
    id: str
    name: str
    email: str
    password_hash: str
    location: str
    latitude: float
    longitude: float
    created_at: datetime
    updated_at: datetime

@dataclass
class Position:
    id: str
    hospital_id: str
    department: str
    title: str
    description: str
    requirements: List[str]
    min_year: str
    stipend: str
    created_at: datetime
    updated_at: datetime

@dataclass
class Message:
    id: str
    sender_id: str
    receiver_id: str
    content: str
    created_at: datetime
    read: bool

@dataclass
class Match:
    id: str
    student_id: str
    position_id: str
    status: str  # 'pending', 'accepted', 'rejected'
    created_at: datetime
    updated_at: datetime 