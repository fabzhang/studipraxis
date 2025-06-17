import sqlite3
import json
from datetime import datetime
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from pathlib import Path

# Get the absolute path to the .env file
env_path = Path("/Users/fabianzhang/Desktop/studipraxis/.env")

# Load environment variables with explicit path
load_dotenv(dotenv_path=env_path)

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

# Debug prints
print("Environment variables:")
print(f"SUPABASE_URL: {supabase_url}")
print(f"SUPABASE_KEY: {supabase_key[:10]}...")  # Only print first 10 chars of key for security

if not supabase_url or not supabase_key:
    raise ValueError("Supabase credentials not found in environment variables")

supabase: Client = create_client(supabase_url, supabase_key)

def export_sqlite_data():
    """Export data from SQLite database."""
    conn = sqlite3.connect("data/studipraxis.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Export students
    cursor.execute("SELECT * FROM students")
    students = [dict(row) for row in cursor.fetchall()]
    
    # Export hospitals
    cursor.execute("SELECT * FROM hospitals")
    hospitals = [dict(row) for row in cursor.fetchall()]
    
    # Export positions
    cursor.execute("SELECT * FROM positions")
    positions = [dict(row) for row in cursor.fetchall()]
    
    # Export matches
    cursor.execute("SELECT * FROM matches")
    matches = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    
    return {
        "students": students,
        "hospitals": hospitals,
        "positions": positions,
        "matches": matches
    }

def import_to_supabase(data):
    """Import data to Supabase."""
    # Import hospitals first (due to foreign key constraints)
    print("Importing hospitals...")
    for hospital in data["hospitals"]:
        try:
            supabase.table("hospitals").insert({
                "id": hospital["id"],
                "name": hospital["name"],
                "email": hospital["email"],
                "password_hash": hospital["password_hash"],
                "location": hospital["location"],
                "latitude": hospital["latitude"],
                "longitude": hospital["longitude"],
                "created_at": hospital["created_at"],
                "updated_at": hospital["updated_at"]
            }).execute()
        except Exception as e:
            print(f"Error importing hospital {hospital['id']}: {e}")
    
    # Import students
    print("Importing students...")
    for student in data["students"]:
        try:
            supabase.table("students").insert({
                "id": student["id"],
                "name": student["name"],
                "email": student["email"],
                "password_hash": student["password_hash"],
                "year": student["year"],
                "interests": student["interests"],
                "praxiserfahrungen": student["praxiserfahrungen"],
                "certifications": student["certifications"],
                "created_at": student["created_at"],
                "updated_at": student["updated_at"]
            }).execute()
        except Exception as e:
            print(f"Error importing student {student['id']}: {e}")
    
    # Import positions
    print("Importing positions...")
    for position in data["positions"]:
        try:
            supabase.table("positions").insert({
                "id": position["id"],
                "hospital_id": position["hospital_id"],
                "department": position["department"],
                "title": position["title"],
                "description": position["description"],
                "requirements": position["requirements"],
                "min_year": position["min_year"],
                "stipend": position["stipend"],
                "created_at": position["created_at"],
                "updated_at": position["updated_at"]
            }).execute()
        except Exception as e:
            print(f"Error importing position {position['id']}: {e}")
    
    # Import matches
    print("Importing matches...")
    for match in data["matches"]:
        try:
            supabase.table("matches").insert({
                "id": match["id"],
                "student_id": match["student_id"],
                "position_id": match["position_id"],
                "status": match["status"],
                "created_at": match["created_at"],
                "updated_at": match["updated_at"]
            }).execute()
        except Exception as e:
            print(f"Error importing match {match['id']}: {e}")

def main():
    print("Starting data migration...")
    
    # Export data from SQLite
    print("Exporting data from SQLite...")
    data = export_sqlite_data()
    
    # Import data to Supabase
    print("Importing data to Supabase...")
    import_to_supabase(data)
    
    print("Migration completed!")

if __name__ == "__main__":
    main() 