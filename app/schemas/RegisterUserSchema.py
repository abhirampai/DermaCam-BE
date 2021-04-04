from pydantic import BaseModel, EmailStr


class RegisterUserSchema(BaseModel):
    firstName:str
    lastName:str
    email: EmailStr
    password: str
    confirmPassword: str
