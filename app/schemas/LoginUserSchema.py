from pydantic import BaseModel,EmailStr

class LoginUserSchema(BaseModel):
    
    email: EmailStr
    password: str