from fastapi import APIRouter
from ..schemas.RegisterUserSchema import RegisterUserSchema
from ..services import user_service

router = APIRouter()

@router.post("/register", response_description="User registration")
def add_user(register_user:RegisterUserSchema):
    return user_service.add_user(register_user)

#@router.post("/login", response_description="User login")