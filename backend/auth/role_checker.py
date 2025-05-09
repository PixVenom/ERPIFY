from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List
from jose import jwt, JWTError
from backend.utils.jwt import SECRET_KEY, ALGORITHM

class JWTBearer(HTTPBearer):
    def __init__(self, allowed_roles: List[str]):
        super(JWTBearer, self).__init__()
        self.allowed_roles = allowed_roles

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            token = credentials.credentials
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                role = payload.get("role")
                if role not in self.allowed_roles:
                    raise HTTPException(status_code=403, detail="Forbidden: Role not authorized")
            except JWTError:
                raise HTTPException(status_code=403, detail="Invalid token or expired")
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization")
