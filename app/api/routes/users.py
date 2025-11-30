from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

router = APIRouter(prefix="/users", tags=["users"])
security = HTTPBasic()
