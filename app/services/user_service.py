from ..db import user_collection
from .auth_service import AuthHandler
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException

auth_service = AuthHandler()

def add_user(user):
    find_user = user_collection.find_one({'email':user.email})
    if(find_user):
        raise HTTPException(status_code=400, detail='Email is already present please sign in')
    elif(user.password != user.confirmPassword):
        raise HTTPException(status_code=400, detail='Password and Confirm password do not match')
    hashed_password = auth_service.get_password_hash(user.password)
    user.password = hashed_password
    del user.confirmPassword
    user_collection.insert_one(jsonable_encoder(user))
    del user.password
    return {"data":user,
    "message":"user created successfully"}