# auth/role_checker.py

from fastapi import Depends, HTTPException
from backend.auth.auth_bearer import JWTBearer
from jose import jwt
from backend.auth.auth_handler import SECRET_KEY, ALGORITHM

def get_current_user(token: str = Depends(JWTBearer())):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # returns a dict: {'sub': 'username', 'role': 'A001'}
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

def admin_required(user=Depends(get_current_user)):
    if user["role"] != "A001":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

def manager_required(user=Depends(get_current_user)):
    if user["role"] not in ("A001", "M001"):
        raise HTTPException(status_code=403, detail="Manager or Admin access required")
    return user
