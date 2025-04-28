from app import create_app, db
from app.models.user import User
from app.models.journal import Journal
from app.models.category import Category, Word
from app.services.liwc_analyzer import LIWCAnalyzer

app = create_app()

with app.app_context():
    print("Creating database tables...")
    db.create_all()
    print("Database tables created successfully!")
    print("Initializing LIWC dictionary...")
    LIWCAnalyzer.initialize_dictionary()
    print("LIWC dictionary initialization complete!")
