from pydantic import BaseModel, EmailStr, model_validator

class AuthRegisterRequest(BaseModel):
    email: EmailStr | None = None
    username: str | None = None
    password: str

    @model_validator(mode="after")
    def require_identifier(self):
        if not self.email and not self.username:
            raise ValueError("email or username is required")
        return self

class AuthLoginRequest(BaseModel):
    email: EmailStr | None = None
    username: str | None = None
    password: str

    @model_validator(mode="after")
    def require_identifier(self):
        if not self.email and not self.username:
            raise ValueError("email or username is required")
        return self

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class MessageResponse(BaseModel):
    message: str
