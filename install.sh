#!/bin/bash
# cPanel-specific installation script for Licensing System
# Optimized for CloudLinux and LiteSpeed
# Usage: curl -s https://raw.githubusercontent.com/iammaksudul/lic/main/install.sh | bash

# Set cPanel-specific paths
ENV="cpanel"
INSTALL_DIR="/home/$(whoami)/public_html/lic"
PYTHON_PATH="/usr/local/cpanel/3rdparty/bin/python3"
PIP_PATH="/usr/local/cpanel/3rdparty/bin/pip3"

echo "Detected environment: $ENV"
echo "Installing to: $INSTALL_DIR"

# Check if directory exists and handle it
if [ -d "$INSTALL_DIR" ]; then
    echo "Directory $INSTALL_DIR already exists."
    read -p "Do you want to continue with the existing directory? (y/n): " CONTINUE
    if [ "$CONTINUE" != "y" ]; then
        echo "Installation aborted."
        exit 1
    fi
    echo "Continuing with existing directory..."
else
    # Create installation directory
    mkdir -p $INSTALL_DIR
fi

# Change to installation directory
cd $INSTALL_DIR

# Create virtual environment using cPanel Python
echo "Creating virtual environment..."
$PYTHON_PATH -m venv venv
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
$PIP_PATH install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file with cPanel-specific settings
echo "Creating .env file..."
cat > .env << EOL
DATABASE_URL=postgresql://chatg_licensing_db:WBBFmmjsn%7Bh%7B@localhost/chatg_licensing_db
SECRET_KEY=95537e8846c4403dce813bfe9572c60c12a7b5f681f6e9401a2abcd8f3c7602e
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
EOL

# Setup PostgreSQL for cPanel
echo "Setting up database for cPanel..."
if command -v createdb &> /dev/null; then
    createdb chatg_licensing_db || echo "Database may already exist."
else
    echo "Warning: 'createdb' command not found. Please create the database manually in cPanel."
fi

# Initialize Alembic
echo "Initializing Alembic..."
alembic init alembic

# Update alembic.ini with database URL
sed -i "s|sqlalchemy.url = driver://user:pass@localhost/dbname|sqlalchemy.url = postgresql://chatg_licensing_db:WBBFmmjsn%7Bh%7B@localhost/chatg_licensing_db|g" alembic.ini

# Run database migrations
echo "Running database migrations..."
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

# Create cPanel-specific management scripts
cat > start.sh << EOL
#!/bin/bash
cd $INSTALL_DIR
source venv/bin/activate
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 > app.log 2>&1 &
echo \$! > app.pid
echo "Application started with PID \$(cat app.pid)"
EOL

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

cat > restart.sh << EOL
#!/bin/bash
./stop.sh
sleep 2
./start.sh
EOL

cat > logs.sh << EOL
#!/bin/bash
tail -f app.log
EOL

# Make scripts executable
chmod +x start.sh stop.sh status.sh restart.sh logs.sh

echo "Installation complete!"
echo "To start the application: ./start.sh"
echo "To stop the application: ./stop.sh"
echo "To check status: ./status.sh"
echo "To restart the application: ./restart.sh"
echo "To view logs: ./logs.sh"
echo "The application will be available at http://$(hostname -I | awk '{print $1}'):8000"
echo "Admin credentials:"
echo "Email: admin"
echo "Password: L1c@dm1n2024$P@ss" 