from pydantic import BaseModel,EmailStr

class RegisterUserSchema(BaseModel):
    
    email: EmailStr
    password: str
    confirmPassword:str