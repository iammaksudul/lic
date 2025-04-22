from app.services.auth import create_user
from app.schemas.user import UserCreate
from app.core.config import settings
from app.db.session import SessionLocal

def create_admin():
    db = SessionLocal()
    try:
        user_data = UserCreate(
            email="admin@example.com",
            password="admin123",
            full_name="System Admin",
            role="admin",
            active=True,
            superuser=True
        )
        user = create_user(db, user_data)
        print(f"Created admin account: {user.email}")
    except Exception as e:
        print(f"Error creating admin: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin() 