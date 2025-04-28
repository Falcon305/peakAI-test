from app import create_app, db
from app.models.user import User
from app.models.journal import Journal
from app.models.category import Category, Word
from app.services.liwc_analyzer import LIWCAnalyzer
from sqlalchemy import inspect
import sys

app = create_app()

def check_if_table_exists(table_name):
    """Check if a table exists in the database"""
    inspector = inspect(db.engine)
    return table_name in inspector.get_table_names()

with app.app_context():
    print("Creating/Updating database tables...")
    db.create_all()
    print("Database tables ready!")
    
    try:
        if check_if_table_exists('categories') and db.session.query(Category).count() > 0:
            print("LIWC dictionary already exists, skipping initialization.")
        else:
            print("Initializing LIWC dictionary...")
            LIWCAnalyzer.initialize_dictionary()
            print("LIWC dictionary initialization complete!")
    except Exception as e:
        print(f"Error checking LIWC dictionary: {e}")
