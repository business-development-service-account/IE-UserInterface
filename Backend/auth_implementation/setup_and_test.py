#!/usr/bin/env python3
"""
Setup and test script for the authentication system.
Run this script to install dependencies and test the authentication implementation.
"""

import os
import sys
import subprocess

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n🔧 {description}")
    print(f"Running: {command}")

    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ Success: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e.stderr.strip()}")
        return False

def main():
    """Main setup and test function."""
    print("🚀 Setting up Authentication System for LangGraph UserInterface")
    print("=" * 60)

    # Change to backend directory
    backend_dir = "/Users/nicholas/Code/Agents/LangGraph/UserInterface/Backend"
    os.chdir(backend_dir)
    print(f"Working directory: {os.getcwd()}")

    # Step 1: Install dependencies
    print("\n📦 Installing dependencies...")
    if not run_command("source venv/bin/activate && pip install -r requirements.txt", "Installing Python dependencies"):
        print("❌ Failed to install dependencies")
        return False

    # Step 2: Apply database migrations
    print("\n🗄️ Applying database migrations...")
    if not run_command("source venv/bin/activate && alembic upgrade head", "Applying Alembic migrations"):
        print("❌ Failed to apply migrations")
        return False

    # Step 3: Test database schema
    print("\n🔍 Testing database schema...")
    if not run_command("sqlite3 app.db '.tables'", "Checking database tables"):
        print("❌ Failed to check database schema")
        return False

    if not run_command("sqlite3 app.db '.schema users' | head -10", "Checking users table schema"):
        print("❌ Failed to check users table schema")
        return False

    # Step 4: Test imports
    print("\n🧪 Testing authentication imports...")
    test_import_script = '''
import sys
sys.path.append('.')

try:
    from auth_implementation.core.security import create_access_token, verify_password, get_password_hash
    from auth_implementation.models.user import User
    from auth_implementation.schemas.user import UserCreate
    from auth_implementation.services.user_service import UserService
    print("✅ All authentication imports successful")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
'''

    if not run_command(f"source venv/bin/activate && python3 -c '{test_import_script}'", "Testing authentication imports"):
        print("❌ Failed authentication imports")
        return False

    # Step 5: Create a simple test
    print("\n🧪 Running basic authentication tests...")
    test_script = '''
import sys
sys.path.append('.')

from auth_implementation.core.security import get_password_hash, verify_password

# Test password hashing
password = "TestPassword123!"
hashed = get_password_hash(password)
verified = verify_password(password, hashed)

if verified:
    print("✅ Password hashing and verification working")
else:
    print("❌ Password hashing/verification failed")
    sys.exit(1)

# Test JWT token creation
try:
    from auth_implementation.core.security import create_access_token, verify_token
    token = create_access_token(subject="test_user")
    payload = verify_token(token, "access")

    if payload == "test_user":
        print("✅ JWT token creation and verification working")
    else:
        print("❌ JWT token verification failed")
        sys.exit(1)
except Exception as e:
    print(f"❌ JWT token test failed: {e}")
    sys.exit(1)

print("✅ All basic authentication tests passed")
'''

    if not run_command(f"source venv/bin/activate && python3 -c '{test_script}'", "Running authentication tests"):
        print("❌ Failed authentication tests")
        return False

    print("\n🎉 Authentication system setup complete!")
    print("\n📋 Summary:")
    print("✅ Dependencies installed")
    print("✅ Database migrations applied")
    print("✅ Authentication models created")
    print("✅ Security utilities working")
    print("✅ JWT tokens working")

    print("\n📝 Next Steps:")
    print("1. Integrate authentication endpoints into main.py")
    print("2. Update frontend to use authentication")
    print("3. Add user-project relationships")
    print("4. Implement audit logging")
    print("5. Add role-based permissions")

    print("\n🔗 Available Authentication Endpoints (once integrated):")
    print("- POST /api/v1/auth/register")
    print("- POST /api/v1/auth/login")
    print("- POST /api/v1/auth/refresh")
    print("- POST /api/v1/auth/logout")
    print("- GET /api/v1/auth/me")
    print("- PUT /api/v1/auth/me")
    print("- POST /api/v1/auth/change-password")

    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)