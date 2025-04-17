from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class StudentProfile:
    id: str
    name: str
    year: int
    interests: List[str]
    availability: str
    certifications: Optional[List[str]]
    created_at: datetime
    updated_at: datetime

@dataclass
class HospitalProfile:
    id: str
    name: str
    department: str
    title: str
    description: str
    duration: str
    requirements: List[str]
    location: str
    latitude: float  # Hamburg coordinates
    longitude: float  # Hamburg coordinates
    stipend: Optional[float]
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
    hospital_id: str
    status: str  # 'pending', 'accepted', 'rejected'
    created_at: datetime
    updated_at: datetime 