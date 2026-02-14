
from fastapi import APIRouter, HTTPException, Header, Body
from ..database import supabase
from pydantic import BaseModel
from typing import Dict, Any, Optional

router = APIRouter()

# Helper: Verify Token (Simplified for illustration)
def get_user_id(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Token")
    token = authorization.replace("Bearer ", "")
    try:
        user = supabase.auth.get_user(token)
        return user.user.id
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Token")

@router.get("/watchlist")
async def get_watchlist(authorization: Optional[str] = Header(None)):
    uid = get_user_id(authorization)
    try:
        res = supabase.table("user_settings").select("watchlist_data").eq("user_id", uid).single().execute()
        return res.data if res.data else {"watchlist_data": None}
    except Exception:
        return {"watchlist_data": None}

@router.post("/watchlist")
async def save_watchlist(watchlist_data: Dict[str, Any] = Body(...), authorization: Optional[str] = Header(None)):
    uid = get_user_id(authorization)
    try:
        # Upsert logic
        payload = {
            "user_id": uid,
            "watchlist_data": watchlist_data,
            "updated_at": "now()"
        }
        res = supabase.table("user_settings").upsert(payload).execute()
        return {"success": True, "data": res.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/portfolio")
async def get_portfolio(authorization: Optional[str] = Header(None)):
    uid = get_user_id(authorization)
    try:
        res = supabase.table("user_settings").select("portfolio_data").eq("user_id", uid).single().execute()
        return res.data if res.data else {"portfolio_data": None}
    except Exception:
        return {"portfolio_data": None}

@router.post("/portfolio")
async def save_portfolio(portfolio_data: Dict[str, Any] = Body(...), authorization: Optional[str] = Header(None)):
    uid = get_user_id(authorization)
    try:
        payload = {
            "user_id": uid,
            "portfolio_data": portfolio_data,
            "updated_at": "now()"
        }
        res = supabase.table("user_settings").upsert(payload).execute()
        return {"success": True, "data": res.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
