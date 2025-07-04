from fastapi import APIRouter, Depends, HTTPException
from typing import List
from backend.models.schemas import UserCreate, UserOut
from backend.auth.role_checker import admin_required
from backend.database import get_connection
from backend.models.schemas import UserCreate, UserOut

router = APIRouter()


@router.post("/users", response_model=UserOut, dependencies=[Depends(admin_required)])
def create_user(user: UserCreate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("INSERT INTO users (user_id, username, password_hash, role_id, created_at) VALUES (%d,%s,%s,%d,%s)",
                   (user.username, user.password_hash, user.role_id))
    conn.commit()
    cursor.execute("SELECT * FROM users WHERE user_id = LAST_INSERT_ID()")
    new_user = cursor.fetchone()
    cursor.close()
    conn.close()
    return new_user

@router.get("/users", response_model=List[UserOut], dependencies=[Depends(admin_required)])
def get_users():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return users


@router.get("/users/{user_id}", response_model=UserOut, dependencies=[Depends(admin_required)])
def get_user(user_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE user_id = %d", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/{user_id}", response_model=UserOut, dependencies=[Depends(admin_required)])
def update_user(user_id: int, user: UserCreate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("UPDATE users SET username=%s, password_hash=%s, role_id=%d WHERE user_id=%d",
                   (user.username, user.password_hash, user.role_id, user_id))
    conn.commit()
    cursor.execute("SELECT * FROM users WHERE user_id = %d", (user_id,))
    updated_user = cursor.fetchone()
    cursor.close()
    conn.close()
    return updated_user


@router.delete("/users/{user_id}", dependencies=[Depends(admin_required)])
def delete_user(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE user_id = %d", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "User deleted successfully"}