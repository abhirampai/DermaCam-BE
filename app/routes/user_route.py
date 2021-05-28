from fastapi import APIRouter, Depends, File, UploadFile
from ..schemas.RegisterUserSchema import RegisterUserSchema, RegisterResponseModel, ResetPasswordSchema
from ..schemas.PatientHealthSchema import PatientHealthSchema, GetHealthStatus
from ..schemas.LoginUserSchema import LoginUserSchema, LoginResponseModel, GetUserResponseModel, ResetPasswordResponseModel
from ..services import (user_service, auth_service,)
from ..db import cloudinary

router = APIRouter()
auth_service = auth_service.AuthHandler()


@router.post("/register", response_description="User registration", response_model=RegisterResponseModel)
def add_user(register_user: RegisterUserSchema):
    return user_service.add_user(register_user)


@router.post("/login", response_description="User login", response_model=LoginResponseModel)
def login_user(login_user: LoginUserSchema):
    return user_service.login_user(login_user)


@router.get('/getUser', response_description="Get Logged in User details", response_model=GetUserResponseModel)
def get_user(userid=Depends(auth_service.auth_wrapper)):
    return user_service.get_user(userid)


@router.post('/patientHealthDetails', response_description="Patients Health Details")
def add_patient_details(patient_data: PatientHealthSchema, userid=Depends(auth_service.auth_wrapper)):
    return user_service.add_patient_details(userid, patient_data)


@router.put('/forgotPassword', response_description="Reset users password", response_model=ResetPasswordResponseModel)
def reset_password(reset_password: ResetPasswordSchema):
    return user_service.reset_password(reset_password)


@router.get('/userHealthDetailStatus', response_description="Check whether user's health details are entered", response_model=GetHealthStatus)
def get_status(userid=Depends(auth_service.auth_wrapper)):
    return user_service.get_health_detail_status(userid)


@router.get('/userHealthDetail', response_description="Get user's health details")
def get_user_health_details(userid=Depends(auth_service.auth_wrapper)):
    return user_service.get_user_health_detail(userid)

@router.post("/uploadImage", response_description="Return The disease to be detected")
async def uploadImage(image: UploadFile = File(...)):
    result = cloudinary.uploader.upload(image.file)
    return user_service.get_user_disease_detail(result['url'])
