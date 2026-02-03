from pydantic import BaseModel, EmailStr

class AuthRegisterRequest(BaseModel):
    email: EmailStr
    password: str

class AuthLoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class MessageResponse(BaseModel):
    message: str
