from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.models.schemas import LoginModel, UserCreate, UserOut
from backend.utils.db import get_connection
from backend.utils.security import hash_password, verify_password
from backend.utils.jwt import create_access_token

router = APIRouter()

# --- Register ---
@router.post("/register", response_model=UserOut)
def register_user(user: UserCreate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Check if username already exists
        cursor.execute("SELECT * FROM users WHERE user_id = %d", (user.username))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Username already exists")

        # Hash password before storing
        hashed = hash_password(user.password_hash)

        cursor.execute(
            "INSERT INTO users (user_id, username, password_hash, role_id,created_at) VALUES (%d, %s, %s,%d,%s)",
            (user.user_id, user.username,user.password_hash,user.role_id,user.created_at)
        )
        conn.commit()

        cursor.execute("SELECT * FROM users WHERE user_id = LAST_INSERT_ID()")
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


# --- Login ---
@router.post("/login")
async def login(user: LoginModel):
    print(f"Logging in: {user.username}")
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM users WHERE username = %s", (user.username,))
        db_user = cursor.fetchone()
        print("User from DB:", db_user)
    finally:
        cursor.close()
        conn.close()

    if db_user is None:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    stored_password_hash = db_user[1]  # double check index
    print("Stored hash:", stored_password_hash)

    if not verify_password(user.password, stored_password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/test-password")
def test_password():
    # Test the hash_password function with a custom password
    custom_password = "admin123"
    hashed_password = hash_password(custom_password)
    
    # Verifying the custom password
    is_valid = verify_password(custom_password, hashed_password)
    
    return {"hashed_password": hashed_password, "is_valid": is_valid}