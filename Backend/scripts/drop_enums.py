"""Drop existing ENUM types from PostgreSQL database"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text
from db.database import engine

def drop_enums():
    """Drop all custom ENUM types"""
    with engine.connect() as conn:
        try:
            # Drop ENUMs in reverse order (in case of dependencies)
            conn.execute(text("DROP TYPE IF EXISTS workouttype CASCADE;"))
            conn.execute(text("DROP TYPE IF EXISTS intensitylevel CASCADE;"))
            conn.execute(text("DROP TYPE IF EXISTS smokinglocation CASCADE;"))
            conn.commit()
            print("✓ All ENUM types dropped successfully")
        except Exception as e:
            print(f"✗ Error dropping ENUMs: {e}")
            conn.rollback()

if __name__ == "__main__":
    drop_enums()
