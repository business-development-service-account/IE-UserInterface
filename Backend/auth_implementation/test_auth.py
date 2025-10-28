#!/usr/bin/env python3
"""
Test script for authentication system functionality.
"""

import os
import sys

# Add paths
sys.path.append('.')
sys.path.append('./auth_implementation')

def test_imports():
    """Test that all authentication modules can be imported."""
    print("🧪 Testing authentication imports...")

    try:
        from auth_implementation.core.security import (
            create_access_token, verify_password, get_password_hash,
            verify_token, create_refresh_token
        )
        print("✅ Security utilities imported successfully")

        from auth_implementation.models.user import User
        from auth_implementation.models.session import UserSession
        print("✅ Models imported successfully")

        from auth_implementation.schemas.user import UserCreate, LoginRequest, Token
        print("✅ Schemas imported successfully")

        from auth_implementation.services.user_service import UserService
        print("✅ Services imported successfully")

        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_password_hashing():
    """Test password hashing and verification."""
    print("\n🔐 Testing password hashing...")

    try:
        from auth_implementation.core.security import get_password_hash, verify_password

        password = "TestPass123!"
        # Ensure password is within bcrypt's 72 byte limit
        password = password[:72]
        hashed = get_password_hash(password)
        verified = verify_password(password, hashed)

        if verified:
            print("✅ Password hashing and verification working")
            return True
        else:
            print("❌ Password verification failed")
            return False
    except Exception as e:
        print(f"❌ Password hashing test failed: {e}")
        return False

def test_jwt_tokens():
    """Test JWT token creation and verification."""
    print("\n🎫 Testing JWT tokens...")

    try:
        from auth_implementation.core.security import create_access_token, verify_token

        token = create_access_token(subject="test_user")
        payload = verify_token(token, "access")

        if payload == "test_user":
            print("✅ JWT token creation and verification working")
            return True
        else:
            print(f"❌ JWT token verification failed. Expected 'test_user', got '{payload}'")
            return False
    except Exception as e:
        print(f"❌ JWT token test failed: {e}")
        return False

def test_schemas():
    """Test Pydantic schemas."""
    print("\n📋 Testing schemas...")

    try:
        from auth_implementation.schemas.user import UserCreate, LoginRequest

        # Test UserCreate schema
        user_data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "TestPassword123!",
            "full_name": "Test User"
        }

        user = UserCreate(**user_data)
        print(f"✅ UserCreate schema working: {user.email}")

        # Test LoginRequest schema
        login_data = {
            "username_or_email": "testuser",
            "password": "TestPassword123!"
        }

        login = LoginRequest(**login_data)
        print(f"✅ LoginRequest schema working: {login.username_or_email}")

        return True
    except Exception as e:
        print(f"❌ Schema test failed: {e}")
        return False

def test_database_connection():
    """Test database connection and models."""
    print("\n🗄️ Testing database connection...")

    try:
        from app.core.database import get_db
        from auth_implementation.models.user import User

        # Test database connection
        db = next(get_db())

        # Test if we can query users table
        user_count = db.query(User).count()
        print(f"✅ Database connection working. Current users: {user_count}")

        db.close()
        return True
    except Exception as e:
        print(f"❌ Database connection test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Testing Authentication System Implementation")
    print("=" * 50)

    # Change to backend directory
    os.chdir('/Users/nicholas/Code/Agents/LangGraph/UserInterface/Backend')

    tests = [
        test_imports,
        test_password_hashing,
        test_jwt_tokens,
        test_schemas,
        test_database_connection
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1

    print("\n" + "=" * 50)
    print(f"🎯 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All authentication tests passed!")
        print("\n📋 Authentication System Status:")
        print("✅ User models created")
        print("✅ Session management ready")
        print("✅ JWT tokens working")
        print("✅ Password security implemented")
        print("✅ API schemas defined")
        print("✅ Database tables created")

        print("\n🔗 Ready for Integration:")
        print("- Add auth endpoints to main.py")
        print("- Update frontend for authentication")
        print("- Implement user-project relationships")

        return True
    else:
        print(f"❌ {total - passed} tests failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)