# not a part of the project, only used for testing API errors

from datetime import timedelta
from auth.auth_handler import create_access_token  # Assuming this is the location of the function
from auth.auth_handler import verify_password
from models.models import User  # Replace with actual user model if needed

# Sample hardcoded credentials (for testing purposes)
sample_user = {
    "username": "admin",
    "password": "admin123"
}

# Test function to verify credentials
def test_verify_password():
    # Assuming you have a hashed password for 'admin123'
    hashed_password = "$2b$12$tf4vzct0zACtgPIAa4K1CukOIvVKu2jA7qR65fW0ARyZ7SuWOcRwG"  # Example hashed password
    password_is_valid = verify_password(sample_user["password"], hashed_password)
    print(f"Password valid: {password_is_valid}")

# Test function to generate JWT token
def test_create_token():
    # Create token with user data (in real scenarios, you would retrieve the data from the DB)
    user_data = {"sub": sample_user["username"], "role": "A001"}  # Example user data
    access_token = create_access_token(user_data, expires_delta=timedelta(minutes=30))
    print(f"Access token: {access_token}")

if __name__ == "__main__":
    test_verify_password()
    test_create_token()