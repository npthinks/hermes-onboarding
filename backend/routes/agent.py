from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
# from services.docker_service import provision_agent
# from services.database import update_user_status, get_user

from backend.services.docker_service import provision_agent
from backend.services.database import update_user_status, get_user

router = APIRouter()

class ProvisionRequest(BaseModel):
    user_id: str

@router.post("/provision")
async def provision(
    request: ProvisionRequest,
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(
        provision_agent,
        request.user_id
    )
    
    update_user_status(request.user_id, "provisioning")
    
    return {
        "status": "provisioning",
        "message": "Your agent is being set up..."
    }

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