from app.db.base import Base
from app.db.session import engine
from app.scripts.create_admin import create_admin
from app.scripts.create_dummy_client import create_dummy_client

def init_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")
    
    print("\nCreating admin account...")
    create_admin()
    print("Admin account created successfully!")
    
    print("\nCreating dummy client account...")
    create_dummy_client()
    print("Dummy client account created successfully!")
    
    print("\nDatabase initialization completed!")

if __name__ == "__main__":
    init_db() 