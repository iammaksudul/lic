#!/bin/bash
# Script to create an admin user
# Usage: bash create-admin.sh

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Please run the installation script first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Create Python script to add admin user
cat > create_admin.py << EOL
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.core.security import get_password_hash
from app.models.user import User, UserRole

def create_admin_user():
    db = SessionLocal()
    try:
        # Check if admin user already exists
        admin = db.query(User).filter(User.email == "admin").first()
        if admin:
            print("Admin user already exists.")
            return
        
        # Create admin user
        admin_user = User(
            email="admin",
            hashed_password=get_password_hash("sabbu@684828/*-"),
            full_name="Administrator",
            role=UserRole.ADMIN,
            is_active=True,
            is_superuser=True
        )
        
        db.add(admin_user)
        db.commit()
        print("Admin user created successfully!")
        print("Email: admin")
        print("Password: sabbu@684828/*-")
    except Exception as e:
        print(f"Error creating admin user: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()
EOL

# Run the Python script
python create_admin.py

# Clean up
rm create_admin.py

echo "Admin user setup complete!" 