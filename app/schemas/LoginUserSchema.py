from pydantic import BaseModel, EmailStr


class LoginUserSchema(BaseModel):

    email: EmailStr
    password: str


class LoginResponseModel(BaseModel):
        token: str

class GetUserResponseModel(BaseModel):
    data = {
        "user_id": "str",
        "email": "user@example.com",
        "firstName": "str",
        "lastName": "str",
    }

class ResetPasswordResponseModel(BaseModel):
    data:EmailStr
    message = "Password reset successfully"