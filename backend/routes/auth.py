from fastapi import APIRouter
from pydantic import BaseModel
import uuid
# from services.database import create_user
from backend.services.database import create_user

router = APIRouter()

class SignupRequest(BaseModel):
    name: str
    telegram_username: str
    phone_number: str

class SignupResponse(BaseModel):
    user_id: str
    status: str
    message: str

@router.post("/signup", response_model=SignupResponse)
async def signup(request: SignupRequest):
    user_id = str(uuid.uuid4())[:8]
    
    create_user(
        user_id=user_id,
        name=request.name,
        telegram_username=request.telegram_username,
        phone_number=request.phone_number
    )
    
    return SignupResponse(
        user_id=user_id,
        status="created",
        message=f"Account created for {request.name}"
    )