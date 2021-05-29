from pydantic import BaseModel, EmailStr


class RegisterUserSchema(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    lat: str
    long: str
    password: str
    confirmPassword: str


class ResetPasswordSchema(BaseModel):
    email: EmailStr
    password: str
    confirmPassword: str


class RegisterResponseModel(BaseModel):
    data = {
        "firstName": "str",
        "lastName": "str",
        "email": "user@example.com"
    }
    message = "user created successfully"
