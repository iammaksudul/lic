#!/bin/bash
# One-line installation for cPanel
# Usage: curl -s https://raw.githubusercontent.com/iammaksudul/lic/main/install-one-line.sh | bash

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print status messages
print_status() {
    echo -e "${GREEN}[*] $1${NC}"
}

# Function to print error messages
print_error() {
    echo -e "${RED}[!] $1${NC}"
}

# Function to print warning messages
print_warning() {
    echo -e "${YELLOW}[!] $1${NC}"
}

# Check if running on cPanel
if [ ! -d "/usr/local/cpanel" ]; then
    print_error "This script is designed for cPanel hosting only."
    exit 1
fi

# Set cPanel-specific paths
INSTALL_DIR="/home/$(whoami)/public_html/lic"
PYTHON_PATH="/usr/local/cpanel/3rdparty/bin/python3"
PIP_PATH="/usr/local/cpanel/3rdparty/bin/pip3"

# Check Python version
if ! command -v $PYTHON_PATH &> /dev/null; then
    print_error "Python 3 not found. Please install Python 3 in cPanel."
    exit 1
fi

# Create and enter installation directory
print_status "Creating installation directory..."
mkdir -p $INSTALL_DIR
cd $INSTALL_DIR

# Clone or update repository
print_status "Cloning repository..."
if [ -d ".git" ]; then
    print_warning "Repository already exists. Updating..."
    git pull || {
        print_error "Failed to update repository."
        exit 1
    }
else
    git clone https://github.com/iammaksudul/lic.git . || {
        print_error "Failed to clone repository."
        exit 1
    }
fi

# Create virtual environment
print_status "Creating virtual environment..."
$PYTHON_PATH -m venv venv || {
    print_error "Failed to create virtual environment."
    exit 1
}
source venv/bin/activate

# Install dependencies
print_status "Installing dependencies..."
$PIP_PATH install -r requirements.txt || {
    print_error "Failed to install dependencies."
    exit 1
}

# Create .env file
print_status "Creating environment configuration..."
cat > .env << EOL
DATABASE_URL=postgresql://chatg_licensing_db:WBBFmmjsn%7Bh%7B@localhost/chatg_licensing_db
SECRET_KEY=95537e8846c4403dce813bfe9572c60c12a7b5f681f6e9401a2abcd8f3c7602e
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
EOL

# Create database in cPanel
print_status "Setting up database..."
if command -v createdb &> /dev/null; then
    createdb chatg_licensing_db 2>/dev/null || print_warning "Database may already exist."
else
    print_warning "Please create the database manually in cPanel:"
    echo "1. Go to cPanel > PostgreSQL Databases"
    echo "2. Create database: chatg_licensing_db"
    echo "3. Create user with password: WBBFmmjsn{h{h"
    echo "4. Add user to database with all privileges"
    echo "Press Enter when done..."
    read
fi

# Initialize Alembic
print_status "Initializing database migrations..."
if [ ! -d "alembic" ]; then
    alembic init alembic || {
        print_error "Failed to initialize Alembic."
        exit 1
    }
    
    # Update alembic.ini
    sed -i "s|sqlalchemy.url = driver://user:pass@localhost/dbname|sqlalchemy.url = postgresql://chatg_licensing_db:WBBFmmjsn%7Bh%7B@localhost/chatg_licensing_db|g" alembic.ini
    
    # Create initial migration
    alembic revision --autogenerate -m "initial migration" || {
        print_error "Failed to create initial migration."
        exit 1
    }
fi

# Run migrations
print_status "Running database migrations..."
alembic upgrade head || {
    print_error "Failed to run migrations."
    exit 1
}

# Create admin user
print_status "Creating admin user..."
cat > create_admin.py << EOL
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.core.security import get_password_hash
from app.models.user import User, UserRole

def create_admin_user():
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.email == "admin").first()
        if admin:
            print("Admin user already exists.")
            return
        
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

# Set permissions
print_status "Setting permissions..."
chmod -R 755 $INSTALL_DIR

# Create management scripts
print_status "Creating management scripts..."

# Start script
cat > start.sh << EOL
#!/bin/bash
cd $INSTALL_DIR
source venv/bin/activate
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 > app.log 2>&1 &
echo \$! > app.pid
echo "Application started with PID \$(cat app.pid)"
EOL

# Stop script
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

# Status script
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

# Logs script
cat > logs.sh << EOL
#!/bin/bash
tail -f app.log
EOL

chmod +x start.sh stop.sh status.sh logs.sh

# Print success message
print_status "Installation complete!"
echo -e "\n${GREEN}Management Commands:${NC}"
echo "To start: ./start.sh"
echo "To stop: ./stop.sh"
echo "To check status: ./status.sh"
echo "To view logs: ./logs.sh"
echo -e "\n${GREEN}API Access:${NC}"
echo "API will be available at: http://$(hostname -I | awk '{print $1}'):8000"
echo -e "\n${GREEN}Admin Credentials:${NC}"
echo "Email: admin"
echo "Password: L1c@dm1n2024$P@ss"
echo -e "\n${YELLOW}Important: Change the admin password after first login!${NC}" 