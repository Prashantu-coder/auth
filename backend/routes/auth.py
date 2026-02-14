
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from ..database import supabase

router = APIRouter()

class UserLogin(BaseModel):
    email: str
    password: str

class UserSignup(BaseModel):
    email: str
    password: str
    full_name: str = None

@router.post("/login")
async def login(user: UserLogin):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": user.email, 
            "password": user.password
        })
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/signup")
async def signup(user: UserSignup):
    try:
        options = {}
        if user.full_name:
            options["data"] = {"full_name": user.full_name}
            
        response = supabase.auth.sign_up({
            "email": user.email, 
            "password": user.password,
            "options": options
        })
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/logout")
async def logout():
    try:
        response = supabase.auth.sign_out()
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
