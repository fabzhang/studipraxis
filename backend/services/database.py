import sqlite3
from pathlib import Path
from typing import List, Optional
from datetime import datetime
import uuid
import json
import hashlib

from shared.types import StudentProfile, HospitalProfile, Message, Match, Position

class DatabaseService:
    def __init__(self):
        self.db_path = Path("data/studipraxis.db")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        """Initialize the database with required tables."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create students table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
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
            
            # Create hospitals table (now as accounts)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS hospitals (
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
            
            # Create positions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS positions (
                    id TEXT PRIMARY KEY,
                    hospital_id TEXT NOT NULL,
                    department TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    duration TEXT NOT NULL,
                    requirements TEXT NOT NULL,  -- JSON array of strings
                    stipend REAL,
                    created_at TIMESTAMP NOT NULL,
                    updated_at TIMESTAMP NOT NULL,
                    FOREIGN KEY (hospital_id) REFERENCES hospitals(id)
                )
            """)
            
            # Create messages table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id TEXT PRIMARY KEY,
                    sender_id TEXT NOT NULL,
                    receiver_id TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP NOT NULL,
                    read BOOLEAN NOT NULL DEFAULT 0,
                    FOREIGN KEY (sender_id) REFERENCES students(id),
                    FOREIGN KEY (receiver_id) REFERENCES hospitals(id)
                )
            """)
            
            # Create matches table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS matches (
                    id TEXT PRIMARY KEY,
                    student_id TEXT NOT NULL,
                    position_id TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TIMESTAMP NOT NULL,
                    updated_at TIMESTAMP NOT NULL,
                    FOREIGN KEY (student_id) REFERENCES students(id),
                    FOREIGN KEY (position_id) REFERENCES positions(id)
                )
            """)
            
            conn.commit()

    def _hash_password(self, password: str) -> str:
        """Hash a password for storing."""
        return hashlib.sha256(password.encode()).hexdigest()

    def _verify_password(self, stored_hash: str, provided_password: str) -> bool:
        """Verify a stored password against a provided password."""
        return stored_hash == self._hash_password(provided_password)

    def _dict_to_student(self, row: tuple) -> StudentProfile:
        """Convert a database row to a StudentProfile object."""
        return StudentProfile(
            id=row[0],
            name=row[1],
            email=row[2],
            password_hash=row[3],
            year=row[4],
            interests=json.loads(row[5]),
            availability=row[6],
            certifications=json.loads(row[7]) if row[7] else None,
            created_at=datetime.fromisoformat(row[8]),
            updated_at=datetime.fromisoformat(row[9])
        )

    def _dict_to_hospital(self, row: tuple) -> HospitalProfile:
        """Convert a database row to a HospitalProfile object."""
        return HospitalProfile(
            id=row[0],
            name=row[1],
            email=row[2],
            password_hash=row[3],
            location=row[4],
            latitude=row[5],
            longitude=row[6],
            created_at=datetime.fromisoformat(row[7]),
            updated_at=datetime.fromisoformat(row[8])
        )

    def _dict_to_message(self, row: tuple) -> Message:
        """Convert a database row to a Message object."""
        return Message(
            id=row[0],
            sender_id=row[1],
            receiver_id=row[2],
            content=row[3],
            created_at=datetime.fromisoformat(row[4]),
            read=bool(row[5])
        )

    def _dict_to_match(self, row: tuple) -> Match:
        """Convert a database row to a Match object."""
        return Match(
            id=row[0],
            student_id=row[1],
            position_id=row[2],
            status=row[3],
            created_at=datetime.fromisoformat(row[4]),
            updated_at=datetime.fromisoformat(row[5])
        )

    def _dict_to_position(self, row: tuple) -> Position:
        """Convert a database row to a Position object."""
        return Position(
            id=row[0],
            hospital_id=row[1],
            department=row[2],
            title=row[3],
            description=row[4],
            duration=row[5],
            requirements=json.loads(row[6]),
            stipend=row[7],
            created_at=datetime.fromisoformat(row[8]),
            updated_at=datetime.fromisoformat(row[9])
        )

    # Student operations
    def create_student(self, student: StudentProfile) -> StudentProfile:
        """Create a new student profile."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            now = datetime.now().isoformat()
            student_id = str(uuid.uuid4())
            
            cursor.execute("""
                INSERT INTO students (id, name, email, password_hash, year, interests,
                                    availability, certifications, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                student_id,
                student.name,
                student.email,
                student.password_hash,
                student.year,
                json.dumps(student.interests),
                student.availability,
                json.dumps(student.certifications) if student.certifications else None,
                now,
                now
            ))
            
            conn.commit()
            return self.get_student(student_id)

    def get_student(self, student_id: str) -> Optional[StudentProfile]:
        """Get a student profile by ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
            row = cursor.fetchone()
            return self._dict_to_student(row) if row else None

    def get_students(self) -> List[StudentProfile]:
        """Get all student profiles."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students")
            return [self._dict_to_student(row) for row in cursor.fetchall()]

    def authenticate_student(self, email: str, password: str) -> Optional[StudentProfile]:
        """Authenticate a student account."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students WHERE email = ?", (email,))
            row = cursor.fetchone()
            
            if row and self._verify_password(row[3], password):
                return self._dict_to_student(row)
            return None

    def create_student_account(self, name: str, email: str, password: str, year: int, 
                             interests: List[str], availability: str, 
                             certifications: Optional[List[str]] = None) -> StudentProfile:
        """Create a new student account."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            now = datetime.now().isoformat()
            student_id = str(uuid.uuid4())
            
            cursor.execute("""
                INSERT INTO students (id, name, email, password_hash, year, interests,
                                    availability, certifications, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                student_id,
                name,
                email,
                self._hash_password(password),
                year,
                json.dumps(interests),
                availability,
                json.dumps(certifications) if certifications else None,
                now,
                now
            ))
            
            conn.commit()
            return self.get_student(student_id)

    # Hospital account operations
    def create_hospital_account(self, name: str, email: str, password: str, location: str, latitude: float, longitude: float) -> HospitalProfile:
        """Create a new hospital account."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            now = datetime.now().isoformat()
            hospital_id = str(uuid.uuid4())
            
            cursor.execute("""
                INSERT INTO hospitals (id, name, email, password_hash, location, 
                                     latitude, longitude, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                hospital_id,
                name,
                email,
                self._hash_password(password),
                location,
                latitude,
                longitude,
                now,
                now
            ))
            
            conn.commit()
            return self.get_hospital(hospital_id)

    def authenticate_hospital(self, email: str, password: str) -> Optional[HospitalProfile]:
        """Authenticate a hospital account."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM hospitals WHERE email = ?", (email,))
            row = cursor.fetchone()
            
            if row and self._verify_password(row[3], password):
                return self._dict_to_hospital(row)
            return None

    def get_hospital(self, hospital_id: str) -> Optional[HospitalProfile]:
        """Get a hospital profile by ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM hospitals WHERE id = ?", (hospital_id,))
            row = cursor.fetchone()
            return self._dict_to_hospital(row) if row else None

    def get_hospitals(self) -> List[HospitalProfile]:
        """Get all hospital profiles."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM hospitals")
            return [self._dict_to_hospital(row) for row in cursor.fetchall()]

    # Position operations
    def create_position(self, position: Position) -> Position:
        """Create a new position."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            now = datetime.now().isoformat()
            position_id = str(uuid.uuid4())
            
            cursor.execute("""
                INSERT INTO positions (id, hospital_id, department, title, description,
                                     duration, requirements, stipend, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                position_id,
                position.hospital_id,
                position.department,
                position.title,
                position.description,
                position.duration,
                json.dumps(position.requirements),
                position.stipend,
                now,
                now
            ))
            
            conn.commit()
            return self.get_position(position_id)

    def get_positions(self, hospital_id: Optional[str] = None) -> List[Position]:
        """Get all positions, optionally filtered by hospital."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if hospital_id:
                cursor.execute("SELECT * FROM positions WHERE hospital_id = ?", (hospital_id,))
            else:
                cursor.execute("SELECT * FROM positions")
            return [self._dict_to_position(row) for row in cursor.fetchall()]

    def get_position(self, position_id: str) -> Optional[Position]:
        """Get a position by ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM positions WHERE id = ?", (position_id,))
            row = cursor.fetchone()
            return self._dict_to_position(row) if row else None

    # Message operations
    def create_message(self, message: Message) -> Message:
        """Create a new message."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            message_id = str(uuid.uuid4())
            
            cursor.execute("""
                INSERT INTO messages (id, sender_id, receiver_id, content,
                                    created_at, read)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                message_id,
                message.sender_id,
                message.receiver_id,
                message.content,
                message.created_at.isoformat(),
                message.read
            ))
            
            conn.commit()
            return self.get_message(message_id)

    def get_message(self, message_id: str) -> Optional[Message]:
        """Get a message by ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM messages WHERE id = ?", (message_id,))
            row = cursor.fetchone()
            return self._dict_to_message(row) if row else None

    def get_messages(self, user_id: str) -> List[Message]:
        """Get all messages for a user."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM messages 
                WHERE sender_id = ? OR receiver_id = ?
                ORDER BY created_at DESC
            """, (user_id, user_id))
            return [self._dict_to_message(row) for row in cursor.fetchall()]

    # Match operations
    def create_match(self, match: Match) -> Match:
        """Create a new match."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            match_id = str(uuid.uuid4())
            now = datetime.now().isoformat()
            
            cursor.execute("""
                INSERT INTO matches (id, student_id, position_id, status,
                                   created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                match_id,
                match.student_id,
                match.position_id,
                match.status,
                now,
                now
            ))
            
            conn.commit()
            return self.get_match(match_id)

    def get_match(self, match_id: str) -> Optional[Match]:
        """Get a match by ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM matches WHERE id = ?", (match_id,))
            row = cursor.fetchone()
            return self._dict_to_match(row) if row else None

    def get_matches(self, user_id: str) -> List[Match]:
        """Get all matches for a user."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM matches 
                WHERE student_id = ? OR position_id = ?
                ORDER BY created_at DESC
            """, (user_id, user_id))
            return [self._dict_to_match(row) for row in cursor.fetchall()]

    def get_match_by_student_and_position(self, student_id: str, position_id: str) -> Optional[Match]:
        """Get a match by student and position IDs."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM matches 
                WHERE student_id = ? AND position_id = ?
            """, (student_id, position_id))
            row = cursor.fetchone()
            return self._dict_to_match(row) if row else None

    def update_match_status(self, match_id: str, status: str) -> Match:
        """Update the status of a match."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            now = datetime.now().isoformat()
            
            cursor.execute("""
                UPDATE matches 
                SET status = ?, updated_at = ?
                WHERE id = ?
            """, (status, now, match_id))
            
            conn.commit()
            return self.get_match(match_id)

    def get_applications_for_position(self, position_id: str) -> List[Match]:
        """Get all applications for a position."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM matches 
                WHERE position_id = ? AND status = 'applied'
                ORDER BY created_at DESC
            """, (position_id,))
            return [self._dict_to_match(row) for row in cursor.fetchall()]

    def get_saved_positions_for_student(self, student_id: str) -> List[Match]:
        """Get all saved positions for a student."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM matches 
                WHERE student_id = ? AND status = 'saved'
                ORDER BY created_at DESC
            """, (student_id,))
            return [self._dict_to_match(row) for row in cursor.fetchall()]

    def get_applied_positions_for_student(self, student_id: str) -> List[Match]:
        """Get all applied positions for a student."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM matches 
                WHERE student_id = ? AND status = 'applied'
                ORDER BY created_at DESC
            """, (student_id,))
            return [self._dict_to_match(row) for row in cursor.fetchall()] 