from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from backend.auth.auth_handler import verify_password, create_access_token, decode_token
import os
import sys
from backend.database import engine
from backend.models.models import Base  # Corrected import
from backend.routes import products
from backend.routes import customers
from backend.routes import orders

sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # Fixed typo here

# ================================
# Hardcoded bcrypt-hashed password for "admin123"
# can be changed in routes/auth.py @router.get
admin_user = {
    "username": "admin",
    "password_hash": "$2b$12$tf4vzct0zACtgPIAa4K1CukOIvVKu2jA7qR65fW0ARyZ7SuWOcRwG",  
    "role_id": "A001"
}
# ================================

Base.metadata.create_all(bind=engine)  # Corrected to use 'Base'

# FastAPI app setup
app = FastAPI()

app.include_router(products.router, tags=["Products"])
app.include_router(customers.router, tags=["Customers"])
app.include_router(orders.router, tags=["Orders"])

# CORS config (adjust origin if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500",
                   "http://localhost:5500",
                   "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")  # Fixed mount directory

# Data models
class LoginModel(BaseModel):
    username: str
    password: str

class User(BaseModel):
    username: str
    role_id: str

@app.post("/login")
async def login(user: LoginModel):
    if user.username != admin_user["username"]:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Verify hashed password
    if not verify_password(user.password, admin_user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Generate JWT token
    access_token = create_access_token(data={"sub": user.username, "role": admin_user["role_id"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/protected")
async def protected_route(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"message": f"Hello, {payload['sub']} (role: {payload['role']})"}

@app.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard():
    file_path = "frontend/dashboard.html"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return HTMLResponse(content=file.read())
    else:
        return HTMLResponse(content="<h1>Error: Dashboard file not found</h1>", status_code=404)