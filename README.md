# License Management System

A comprehensive system for managing software licenses, activations, and client access with role-based authentication.

## Features

- **User Authentication & Authorization**
  - Role-based access control (Admin, Client, Public)
  - Secure login and registration
  - JWT token authentication

- **License Management**
  - Create and manage different license types
  - Track license activations
  - Hardware binding for licenses
  - License expiration management

- **Client Management**
  - Client dashboard with license overview
  - License activation tracking
  - Payment management

- **Admin Dashboard**
  - User management
  - License type configuration
  - System analytics
  - Documentation management

- **Security Features**
  - Rate limiting
  - IP whitelisting
  - CORS support
  - Password hashing with bcrypt

## System URLs

- **Public URL**: `http://localhost:8000/`
  - Homepage with feature overview
  - License types information
  - License activation page
  - Registration and login links

- **Client URL**: `http://localhost:8000/client`
  - Client dashboard
  - License management
  - Activation tracking
  - Profile settings
  - Payment management

- **Admin URL**: `http://localhost:8000/admin`
  - Admin dashboard
  - User management
  - License type configuration
  - System analytics
  - Documentation

## Default Accounts

### Admin Account
- **Email**: admin@example.com
- **Password**: admin123
- **URL**: http://localhost:8000/admin/login

### Client Account (Dummy)
- **Email**: client@example.com
- **Password**: client123
- **URL**: http://localhost:8000/login

## Requirements

- Python 3.8+
- PostgreSQL
- pip (Python package manager)

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd license-management-system
   ```

2. **Create a virtual environment and activate it**:
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file** in the root directory with the following variables:
   ```
   DATABASE_URL=postgresql://user:password@localhost:5432/licensing_db
   SECRET_KEY=your-secret-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   RATE_LIMIT=100
   RATE_LIMIT_TIME_WINDOW=60
   IP_WHITELIST_ENABLED=false
   BACKEND_CORS_ORIGINS=["http://localhost:8000"]
   ```

5. **Initialize the database**:
   ```bash
   alembic upgrade head
   ```

6. **Create the admin user**:
   ```bash
   python -m app.scripts.create_admin
   ```

7. **Create a dummy client account**:
   ```bash
   python -m app.scripts.create_dummy_client
   ```

## Running the Application

Start the server with:
```bash
uvicorn app.main:app --reload
```

The application will be available at `http://localhost:8000`.

## API Documentation

Once the server is running, you can access:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Client Documentation

Client documentation is available at:
- **Client Guide**: `http://localhost:8000/client/documentation`
- **API Integration**: `http://localhost:8000/client/documentation/api`

## Admin Documentation

Admin documentation is available at:
- **Admin Guide**: `http://localhost:8000/admin/documentation`
- **System Configuration**: `http://localhost:8000/admin/documentation/configuration`

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure PostgreSQL is running
   - Check your database credentials in the `.env` file
   - Verify the database exists

2. **Authentication Issues**
   - Clear browser cookies and cache
   - Ensure you're using the correct credentials
   - Check if the user account is active

3. **License Activation Problems**
   - Verify the license key is valid
   - Check if the license has expired
   - Ensure the hardware ID is correctly formatted

## Support

For support, please contact:
- Email: support@example.com
- Documentation: http://localhost:8000/docs

## License

This project is licensed under the MIT License - see the LICENSE file for details. 