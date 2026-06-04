from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from backend.services.database import update_user_status, get_user
from backend.services.twilio_service import send_welcome_sms
import asyncio

router = APIRouter()

class ProvisionRequest(BaseModel):
    user_id: str

@router.post("/provision")
async def provision(
    request: ProvisionRequest,
    background_tasks: BackgroundTasks
):
    update_user_status(request.user_id, "provisioning")
    background_tasks.add_task(
        provision_and_notify,
        request.user_id
    )
    
    return {
        "status": "provisioning",
        "message": "Your agent is being set up..."
    }

async def provision_and_notify(user_id: str):
    await asyncio.sleep(8)
    
    user = get_user(user_id)
    if user and user.get("phone_number"):
        try:
            send_welcome_sms(
                to_number=user["phone_number"],
                user_name=user["name"]
            )
        except Exception as e:
            print(f"SMS failed: {str(e)}")
    
    update_user_status(user_id, "ready")
    print(f"User {user_id} status updated to ready")

@router.get("/status/{user_id}")
async def get_status(user_id: str):
    user = get_user(user_id)
    
    if not user:
        return {"status": "not_found"}
    
    return {
        "status": user["status"],
        "user_id": user_id,
        "name": user["name"]
    }