from fastapi import APIRouter, Request
from services.database import get_user_by_telegram, update_user_status
#from backend.services.database import get_user_by_telegram, update_user_status

router = APIRouter()

@router.post("/{user_id}")
async def receive_message(user_id: str, request: Request):
    body = await request.json()
    message = body.get("message", "")
    
    user = get_user_by_telegram(user_id)
    
    if not user:
        return {"status": "user_not_found"}
    
    update_user_status(user_id, "active")
    
    return {
        "status": "received",
        "user_id": user_id,
        "message": message
    }

@router.post("/telegram/pairing/{user_id}")
async def pairing_callback(user_id: str, request: Request):
    body = await request.json()
    pairing_code = body.get("pairing_code", "")
    
    update_user_status(user_id, "pairing")
    
    return {
        "status": "pairing",
        "code": pairing_code
    }