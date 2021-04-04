from fastapi import APIRouter, Depends
from ..schemas.RegisterUserSchema import RegisterUserSchema,RegisterResponseModel
from ..schemas.LoginUserSchema import LoginUserSchema,LoginResponseModel,GetUserResponseModel,ResetPasswordResponseModel
from ..services import (user_service, auth_service,)

router = APIRouter()
auth_service = auth_service.AuthHandler()


@router.post("/register", response_description="User registration",response_model=RegisterResponseModel)
def add_user(register_user: RegisterUserSchema):
    return user_service.add_user(register_user)


@router.post("/login", response_description="User login",response_model=LoginResponseModel)
def login_user(login_user: LoginUserSchema):
    return user_service.login_user(login_user)


@router.get('/getUser', response_description="Get Logged in User details", response_model=GetUserResponseModel)
def get_user(userid=Depends(auth_service.auth_wrapper)):
    return user_service.get_user(userid)


@router.put('/forgotPassword', response_description="Reset users password", response_model=ResetPasswordResponseModel)
def reset_password(reset_password: RegisterUserSchema):
    return user_service.reset_password(reset_password)
