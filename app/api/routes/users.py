from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.models.schemas import UserCreate, ActivationRequest
from app.services.user_service import create_user, activate_user, ConflictError

router = APIRouter(prefix="/users", tags=["users"])
security = HTTPBasic()

@router.post("", status_code=status.HTTP_201_CREATED)
def register_user(payload: UserCreate):
    try:
        create_user(payload.email, payload.password)
    except ConflictError as e:
        raise HTTPException(status_code=409, detail=str(e))
    return {"message": "User created. Check your email for activation code."}
    
@router.post("/activate")
def activate(payload: ActivationRequest, creds: HTTPBasicCredentials = Depends(security)):
    ok = activate_user(creds.username, creds.password, payload.code)
    if not ok:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired code",
        )
    return {"message": "Account activated"}