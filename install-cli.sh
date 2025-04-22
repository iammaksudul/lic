#!/bin/bash
# cPanel-specific installation script for Licensing System
# Optimized for CloudLinux and LiteSpeed
# Usage: curl -s https://raw.githubusercontent.com/iammaksudul/lic/main/install-cli.sh | bash

# Set cPanel-specific paths
INSTALL_DIR="/home/$(whoami)/public_html/lic"
PYTHON_PATH="/usr/local/cpanel/3rdparty/bin/python3"
PIP_PATH="/usr/local/cpanel/3rdparty/bin/pip3"

# Create installation directory
mkdir -p $INSTALL_DIR

# Clone the repository
git clone https://github.com/iammaksudul/lic.git $INSTALL_DIR

# Change to installation directory
cd $INSTALL_DIR

# Create virtual environment using cPanel Python
$PYTHON_PATH -m venv venv
source venv/bin/activate

# Install dependencies
$PIP_PATH install -r requirements.txt

# Create database in cPanel
echo "Please create the database in cPanel:"
echo "1. Go to cPanel > PostgreSQL Databases"
echo "2. Create a new database named 'chatg_licensing_db'"
echo "3. Create a new user with password 'WBBFmmjsn{h{h'"
echo "4. Add the user to the database with all privileges"
echo "Press Enter when done..."
read

# Create .env file
cat > .env << EOL
DATABASE_URL=postgresql://chatg_licensing_db:WBBFmmjsn%7Bh%7B@localhost/chatg_licensing_db
SECRET_KEY=95537e8846c4403dce813bfe9572c60c12a7b5f681f6e9401a2abcd8f3c7602e
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
EOL

# Run database migrations
alembic upgrade head

# Create admin user
echo "Creating admin user..."
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
            hashed_password=get_password_hash("L1c@dm1n2024$P@ss"),
            full_name="Administrator",
            role=UserRole.ADMIN,
            is_active=True,
            is_superuser=True
        )
        
        db.add(admin_user)
        db.commit()
        print("Admin user created successfully!")
        print("Email: admin")
        print("Password: L1c@dm1n2024$P@ss")
    except Exception as e:
        print(f"Error creating admin user: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()
EOL

python create_admin.py
rm create_admin.py

# Set permissions for cPanel
chmod -R 755 $INSTALL_DIR

# Create startup script
cat > start.sh << EOL
#!/bin/bash
cd $INSTALL_DIR
source venv/bin/activate
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 > app.log 2>&1 &
echo \$! > app.pid
echo "Application started with PID \$(cat app.pid)"
EOL

chmod +x start.sh

# Create stop script
cat > stop.sh << EOL
#!/bin/bash
if [ -f app.pid ]; then
    pid=\$(cat app.pid)
    if ps -p \$pid > /dev/null; then
        kill \$pid
        rm app.pid
        echo "Application stopped"
    else
        echo "Application is not running"
        rm app.pid
    fi
else
    echo "PID file not found"
fi
EOL

chmod +x stop.sh

# Create status script
cat > status.sh << EOL
#!/bin/bash
if [ -f app.pid ]; then
    pid=\$(cat app.pid)
    if ps -p \$pid > /dev/null; then
        echo "Application is running (PID: \$pid)"
    else
        echo "Application is not running (stale PID file)"
    fi
else
    echo "Application is not running"
fi
EOL

chmod +x status.sh

# Create logs script
cat > logs.sh << EOL
#!/bin/bash
tail -f app.log
EOL

chmod +x logs.sh

echo "Installation complete!"
echo "To start the application: ./start.sh"
echo "To stop the application: ./stop.sh"
echo "To check status: ./status.sh"
echo "To view logs: ./logs.sh"
echo "The application will be available at http://$(hostname -I | awk '{print $1}'):8000"
echo "Admin credentials:"
echo "Email: admin"
echo "Password: L1c@dm1n2024$P@ss" 