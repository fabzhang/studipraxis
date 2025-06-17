import os
import json
from datetime import datetime
from supabase import create_client, Client
from shared.types import StudentProfile, HospitalProfile, Position, Match

class DatabaseService:
    def __init__(self):
        """Initialize database connection."""
        # Get Supabase credentials from environment variables
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("Supabase credentials not found in environment variables")
            
        # Initialize Supabase client
        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
    
    def get_connection(self):
        """Get database connection."""
        return self.supabase
    
    def create_student(self, student: StudentProfile) -> StudentProfile:
        """Create a new student profile."""
        try:
            data = {
                "id": student.id,
                "name": student.name,
                "email": student.email,
                "password_hash": student.password_hash,
                "year": student.year,
                "interests": json.dumps(student.interests),
                "praxiserfahrungen": student.praxiserfahrungen,
                "certifications": json.dumps(student.certifications) if student.certifications else None,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            
            result = self.supabase.table("students").insert(data).execute()
            return student
        except Exception as e:
            print(f"Error creating student: {e}")
            raise
    
    def get_student(self, student_id: str) -> StudentProfile:
        """Get a student profile by ID."""
        try:
            result = self.supabase.table("students").select("*").eq("id", student_id).execute()
            if result.data:
                row = result.data[0]
                return StudentProfile(
                    id=row["id"],
                    name=row["name"],
                    email=row["email"],
                    password_hash=row["password_hash"],
                    year=row["year"],
                    interests=json.loads(row["interests"]) if row["interests"] else [],
                    praxiserfahrungen=row["praxiserfahrungen"],
                    certifications=json.loads(row["certifications"]) if row["certifications"] else [],
                    created_at=row["created_at"],
                    updated_at=row["updated_at"]
                )
            return None
        except Exception as e:
            print(f"Error getting student: {e}")
            return None
    
    def get_all_students(self) -> list[StudentProfile]:
        """Get all student profiles."""
        try:
            result = self.supabase.table("students").select("*").execute()
            students = []
            for row in result.data:
                students.append(StudentProfile(
                    id=row["id"],
                    name=row["name"],
                    email=row["email"],
                    password_hash=row["password_hash"],
                    year=row["year"],
                    interests=json.loads(row["interests"]) if row["interests"] else [],
                    praxiserfahrungen=row["praxiserfahrungen"],
                    certifications=json.loads(row["certifications"]) if row["certifications"] else [],
                    created_at=row["created_at"],
                    updated_at=row["updated_at"]
                ))
            return students
        except Exception as e:
            print(f"Error getting all students: {e}")
            return []
    
    def update_student(self, student_id: str, **kwargs) -> StudentProfile:
        """Update a student profile."""
        try:
            # Convert lists to JSON strings
            if "interests" in kwargs:
                kwargs["interests"] = json.dumps(kwargs["interests"])
            if "certifications" in kwargs:
                kwargs["certifications"] = json.dumps(kwargs["certifications"])
            
            kwargs["updated_at"] = datetime.now().isoformat()
            
            result = self.supabase.table("students").update(kwargs).eq("id", student_id).execute()
            if result.data:
                return self.get_student(student_id)
            return None
        except Exception as e:
            print(f"Error updating student: {e}")
            return None
    
    def create_hospital(self, hospital: HospitalProfile) -> HospitalProfile:
        """Create a new hospital profile."""
        try:
            data = {
                "id": hospital.id,
                "name": hospital.name,
                "email": hospital.email,
                "password_hash": hospital.password_hash,
                "location": hospital.location,
                "latitude": hospital.latitude,
                "longitude": hospital.longitude,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            
            result = self.supabase.table("hospitals").insert(data).execute()
            return hospital
        except Exception as e:
            print(f"Error creating hospital: {e}")
            raise
    
    def get_hospital(self, hospital_id: str) -> HospitalProfile:
        """Get a hospital profile by ID."""
        try:
            result = self.supabase.table("hospitals").select("*").eq("id", hospital_id).execute()
            if result.data:
                row = result.data[0]
                return HospitalProfile(
                    id=row["id"],
                    name=row["name"],
                    email=row["email"],
                    password_hash=row["password_hash"],
                    location=row["location"],
                    latitude=row["latitude"],
                    longitude=row["longitude"],
                    created_at=row["created_at"],
                    updated_at=row["updated_at"]
                )
            return None
        except Exception as e:
            print(f"Error getting hospital: {e}")
            return None
    
    def get_hospitals(self) -> list[HospitalProfile]:
        """Get all hospital profiles."""
        try:
            result = self.supabase.table("hospitals").select("*").execute()
            hospitals = []
            for row in result.data:
                hospitals.append(HospitalProfile(
                    id=row["id"],
                    name=row["name"],
                    email=row["email"],
                    password_hash=row["password_hash"],
                    location=row["location"],
                    latitude=row["latitude"],
                    longitude=row["longitude"],
                    created_at=row["created_at"],
                    updated_at=row["updated_at"]
                ))
            return hospitals
        except Exception as e:
            print(f"Error getting hospitals: {e}")
            return []
    
    def update_hospital(self, hospital_id: str, **kwargs) -> HospitalProfile:
        """Update a hospital profile."""
        try:
            kwargs["updated_at"] = datetime.now().isoformat()
            
            result = self.supabase.table("hospitals").update(kwargs).eq("id", hospital_id).execute()
            if result.data:
                return self.get_hospital(hospital_id)
            return None
        except Exception as e:
            print(f"Error updating hospital: {e}")
            return None
    
    def create_position(self, position: Position) -> Position:
        """Create a new position."""
        try:
            data = {
                "id": position.id,
                "hospital_id": position.hospital_id,
                "department": position.department,
                "title": position.title,
                "description": position.description,
                "requirements": json.dumps(position.requirements),
                "min_year": position.min_year,
                "stipend": position.stipend,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            
            result = self.supabase.table("positions").insert(data).execute()
            return position
        except Exception as e:
            print(f"Error creating position: {e}")
            raise
    
    def get_position(self, position_id: str) -> Position:
        """Get a position by ID."""
        try:
            result = self.supabase.table("positions").select("*").eq("id", position_id).execute()
            if result.data:
                row = result.data[0]
                return Position(
                    id=row["id"],
                    hospital_id=row["hospital_id"],
                    department=row["department"],
                    title=row["title"],
                    description=row["description"],
                    requirements=json.loads(row["requirements"]) if row["requirements"] else [],
                    min_year=row["min_year"],
                    stipend=row["stipend"],
                    created_at=row["created_at"],
                    updated_at=row["updated_at"]
                )
            return None
        except Exception as e:
            print(f"Error getting position: {e}")
            return None
    
    def get_positions(self, hospital_id: str = None) -> list[Position]:
        """Get all positions, optionally filtered by hospital."""
        try:
            query = self.supabase.table("positions").select("*")
            if hospital_id:
                query = query.eq("hospital_id", hospital_id)
            
            result = query.execute()
            positions = []
            for row in result.data:
                positions.append(Position(
                    id=row["id"],
                    hospital_id=row["hospital_id"],
                    department=row["department"],
                    title=row["title"],
                    description=row["description"],
                    requirements=json.loads(row["requirements"]) if row["requirements"] else [],
                    min_year=row["min_year"],
                    stipend=row["stipend"],
                    created_at=row["created_at"],
                    updated_at=row["updated_at"]
                ))
            return positions
        except Exception as e:
            print(f"Error getting positions: {e}")
            return []
    
    def update_position(self, position: Position) -> Position:
        """Update a position."""
        try:
            data = {
                "department": position.department,
                "title": position.title,
                "description": position.description,
                "requirements": json.dumps(position.requirements),
                "min_year": position.min_year,
                "stipend": position.stipend,
                "updated_at": datetime.now().isoformat()
            }
            
            result = self.supabase.table("positions").update(data).eq("id", position.id).execute()
            if result.data:
                return self.get_position(position.id)
            return None
        except Exception as e:
            print(f"Error updating position: {e}")
            return None
    
    def delete_position(self, position_id: str) -> bool:
        """Delete a position."""
        try:
            result = self.supabase.table("positions").delete().eq("id", position_id).execute()
            return True
        except Exception as e:
            print(f"Error deleting position: {e}")
            return False
    
    def create_match(self, match: Match) -> Match:
        """Create a new match."""
        try:
            data = {
                "id": match.id,
                "student_id": match.student_id,
                "position_id": match.position_id,
                "status": match.status,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            
            result = self.supabase.table("matches").insert(data).execute()
            return match
        except Exception as e:
            print(f"Error creating match: {e}")
            raise
    
    def get_match(self, match_id: str) -> Match:
        """Get a match by ID."""
        try:
            result = self.supabase.table("matches").select("*").eq("id", match_id).execute()
            if result.data:
                row = result.data[0]
                return Match(
                    id=row["id"],
                    student_id=row["student_id"],
                    position_id=row["position_id"],
                    status=row["status"],
                    created_at=row["created_at"],
                    updated_at=row["updated_at"]
                )
            return None
        except Exception as e:
            print(f"Error getting match: {e}")
            return None
    
    def get_match_by_student_and_position(self, student_id: str, position_id: str) -> Match:
        """Get a match by student and position IDs."""
        try:
            result = self.supabase.table("matches").select("*").eq("student_id", student_id).eq("position_id", position_id).execute()
            if result.data:
                row = result.data[0]
                return Match(
                    id=row["id"],
                    student_id=row["student_id"],
                    position_id=row["position_id"],
                    status=row["status"],
                    created_at=row["created_at"],
                    updated_at=row["updated_at"]
                )
            return None
        except Exception as e:
            print(f"Error getting match by student and position: {e}")
            return None
    
    def get_applied_positions_for_student(self, student_id: str) -> list[Match]:
        """Get all applied positions for a student."""
        try:
            result = self.supabase.table("matches").select("*").eq("student_id", student_id).eq("status", "applied").execute()
            matches = []
            for row in result.data:
                matches.append(Match(
                    id=row["id"],
                    student_id=row["student_id"],
                    position_id=row["position_id"],
                    status=row["status"],
                    created_at=row["created_at"],
                    updated_at=row["updated_at"]
                ))
            return matches
        except Exception as e:
            print(f"Error getting applied positions: {e}")
            return []
    
    def get_saved_positions_for_student(self, student_id: str) -> list[Match]:
        """Get all saved positions for a student."""
        try:
            result = self.supabase.table("matches").select("*").eq("student_id", student_id).eq("status", "saved").execute()
            matches = []
            for row in result.data:
                matches.append(Match(
                    id=row["id"],
                    student_id=row["student_id"],
                    position_id=row["position_id"],
                    status=row["status"],
                    created_at=row["created_at"],
                    updated_at=row["updated_at"]
                ))
            return matches
        except Exception as e:
            print(f"Error getting saved positions: {e}")
            return []
    
    def get_applications_for_position(self, position_id: str) -> list[Match]:
        """Get all applications for a position."""
        try:
            result = self.supabase.table("matches").select("*").eq("position_id", position_id).eq("status", "applied").execute()
            matches = []
            for row in result.data:
                matches.append(Match(
                    id=row["id"],
                    student_id=row["student_id"],
                    position_id=row["position_id"],
                    status=row["status"],
                    created_at=row["created_at"],
                    updated_at=row["updated_at"]
                ))
            return matches
        except Exception as e:
            print(f"Error getting applications for position: {e}")
            return []
    
    def update_match_status(self, match_id: str, status: str) -> Match:
        """Update a match's status."""
        try:
            data = {
                "status": status,
                "updated_at": datetime.now().isoformat()
            }
            
            result = self.supabase.table("matches").update(data).eq("id", match_id).execute()
            if result.data:
                return self.get_match(match_id)
            return None
        except Exception as e:
            print(f"Error updating match status: {e}")
            return None
    
    def delete_match(self, match_id: str) -> bool:
        """Delete a match."""
        try:
            result = self.supabase.table("matches").delete().eq("id", match_id).execute()
            return True
        except Exception as e:
            print(f"Error deleting match: {e}")
            return False 