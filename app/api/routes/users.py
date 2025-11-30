from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.models.schemas import UserCreate, ActivationRequest

router = APIRouter(prefix="/users", tags=["users"])
security = HTTPBasic()

@router.post("", status_code=status.HTTP_201_CREATED)
def register_user(payload: UserCreate):
    try:
        # Business logic - create user
        return {"message": "User created. Check your email for activation code."}
    except Exception as e:
        raise HTTPException(status_code=409, detail=str(e))
    
@router.post("/activate")
def activate(payload: ActivationRequest, creds: HTTPBasicCredentials = Depends(security)):
    # Business logic - activate user
    return {"message": "Account activated"}