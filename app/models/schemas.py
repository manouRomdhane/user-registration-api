from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

class ActivationRequest(BaseModel):
    code: str = Field(pattern=r"^\d{4}$")