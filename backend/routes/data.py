
from fastapi import APIRouter, HTTPException, Header, Body
from typing import Dict, Any
from ..database import supabase

router = APIRouter()

# Helper to verify token and get user_id
def get_user_from_token(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization Header")
    
    token = authorization.replace("Bearer ", "")
    user = supabase.auth.get_user(token)
    
    if not user or not user.user:
        raise HTTPException(status_code=401, detail="Invalid Token")
        
    return user.user

@router.get("/watchlist")
async def get_watchlist(authorization: str = Header(None)):
    user = get_user_from_token(authorization)
    try:
        response = supabase.table("user_settings").select("watchlist_data").eq("user_id", user.id).single().execute()
        # Supabase-py returns a response object with 'data'
        if not response.data:
             return {"watchlist_data": None}
        return response.data
    except Exception as e:
        # If no row found, return empty
        return {"watchlist_data": None}

@router.post("/watchlist")
async def save_watchlist(data: Dict[str, Any] = Body(...), authorization: str = Header(None)):
    user = get_user_from_token(authorization)
    try:
        payload = {
            "user_id": user.id,
            "watchlist_data": data,
            "updated_at": "now()" # Let Supabase handle timestamp or pass from frontend
        }
        response = supabase.table("user_settings").upsert(payload, on_conflict="user_id").execute()
        return response.data
    except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))

@router.get("/portfolio")
async def get_portfolio(authorization: str = Header(None)):
    user = get_user_from_token(authorization)
    try:
        response = supabase.table("user_settings").select("portfolio_data").eq("user_id", user.id).single().execute()
        if not response.data:
             return {"portfolio_data": None}
        return response.data
    except Exception as e:
        return {"portfolio_data": None}

@router.post("/portfolio")
async def save_portfolio(data: Dict[str, Any] = Body(...), authorization: str = Header(None)):
    user = get_user_from_token(authorization)
    try:
        payload = {
            "user_id": user.id,
            "portfolio_data": data,
            "updated_at": "now()"
        }
        response = supabase.table("user_settings").upsert(payload, on_conflict="user_id").execute()
        return response.data
    except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))
