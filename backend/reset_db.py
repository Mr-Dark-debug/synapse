"""
Database Reset Script
Run this script when you need to reset the database with a fresh schema.
This is useful after adding new columns to existing tables.

IMPORTANT: This will DELETE all existing data!
"""
import os
from db.session import engine, Base
from db.models import User, Profile, Collection, CollectionItem, PromptTemplate

def reset_database():
    db_path = "synapse.db"
    
    # Check if database exists
    if os.path.exists(db_path):
        print(f"⚠️  Warning: {db_path} will be deleted!")
        # confirm = input("Are you sure you want to continue? (yes/no): ")
        # if confirm.lower() != "yes":
        #     print("❌ Database reset cancelled.")
        #     return
        
        # Delete the database file
        try:
            os.remove(db_path)
            print(f"✅ Deleted old database: {db_path}")
        except Exception as e:
            print(f"❌ Error deleting database: {e}")
            return
    
    # Create all tables with new schema
    Base.metadata.create_all(bind=engine)
    print("✅ Database recreated with latest schema!")
    print("\nℹ️  You can now start the backend server.")

if __name__ == "__main__":
    reset_database()
