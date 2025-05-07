from datetime import datetime, timedelta
from jose import JWTError, jwt

# Secret key and algorithm
SECRET_KEY = "5f0fae80f8c8f959252dc14264117c0684aa1bbddd5e6156be13a01f0b92f84c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 9999999999999999999999999999999999999999999999999999999999999999999999999999999

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt