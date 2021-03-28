from fastapi import APIRouter,Depends
from ..schemas.RegisterUserSchema import RegisterUserSchema
from ..schemas.LoginUserSchema import LoginUserSchema
from ..services import (user_service,auth_service,)

router = APIRouter()
auth_service = auth_service.AuthHandler()

@router.post("/register", response_description="User registration")
def add_user(register_user:RegisterUserSchema):
    return user_service.add_user(register_user)

@router.post("/login", response_description="User login")
def login_user(login_user:LoginUserSchema):
    return user_service.login_user(login_user)

@router.get('/getUser')
def get_user(userid=Depends(auth_service.auth_wrapper)):
    return user_service.get_user(userid)