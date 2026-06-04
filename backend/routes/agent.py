from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
#from services.database import update_user_status, get_user
from backend.services.database import update_user_status, get_user
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
        simulate_provisioning,
        request.user_id
    )
    
    return {
        "status": "provisioning",
        "message": "Your agent is being set up..."
    }

async def simulate_provisioning(user_id: str):
    await asyncio.sleep(5)
    update_user_status(user_id, "ready")

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