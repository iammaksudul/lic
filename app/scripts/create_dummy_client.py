from app.db.session import SessionLocal
from app.schemas.user import UserCreate
from app.crud.user import create_user

def create_dummy_client():
    db = SessionLocal()
    try:
        user_in = UserCreate(
            email="client@example.com",
            password="client123",
            full_name="Dummy Client",
            role="client",
            is_active=True,
            is_superuser=False
        )
        user = create_user(db, user_in)
        print(f"Created dummy client account with email: {user.email}")
    except Exception as e:
        print(f"Error creating dummy client account: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    create_dummy_client() 