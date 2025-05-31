import sqlite3
from pathlib import Path
from datetime import datetime

def migrate_position_schema():
    print("Starting migration of positions table...")
    
    # Connect to the database
    db_path = Path("data/studipraxis.db")
    if not db_path.exists():
        print("Database file not found!")
        return
    
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        # Create new positions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS positions_new (
                id TEXT PRIMARY KEY,
                hospital_id TEXT NOT NULL,
                department TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                requirements TEXT NOT NULL,
                min_year TEXT NOT NULL,
                stipend TEXT,
                created_at TIMESTAMP NOT NULL,
                updated_at TIMESTAMP NOT NULL,
                FOREIGN KEY (hospital_id) REFERENCES hospitals(id)
            )
        """)
        
        # Get existing positions
        cursor.execute("SELECT * FROM positions")
        positions = cursor.fetchall()
        
        # Migrate positions to new schema
        for position in positions:
            cursor.execute("""
                INSERT INTO positions_new (id, hospital_id, department, title, description,
                                         requirements, min_year, stipend, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                position[0],  # id
                position[1],  # hospital_id
                position[2],  # department
                position[3],  # title
                position[4],  # description
                position[5],  # requirements
                position[6],  # min_year
                position[7],  # stipend
                position[8],  # created_at
                position[9]   # updated_at
            ))
        
        # Drop old table and rename new one
        cursor.execute("DROP TABLE positions")
        cursor.execute("ALTER TABLE positions_new RENAME TO positions")
        
        conn.commit()
        print("Migration completed successfully!")

if __name__ == "__main__":
    migrate_position_schema() 