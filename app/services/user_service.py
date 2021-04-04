from ..db import user_collection
from .auth_service import AuthHandler
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from bson.objectid import ObjectId


auth_service = AuthHandler()


def user_helper(user) -> dict:
    return {
        "user_id": str(user["_id"]),
        "email": user["email"],
        "firstName": user["firstName"],
        "lastName": user["lastName"],
    }


def add_user(user):
    find_user = user_collection.find_one({'email': user.email})
    if(find_user):
        raise HTTPException(status_code=400,
                            detail='Email is already present please sign in')
    elif(user.password != user.confirmPassword):
        raise HTTPException(
            status_code=400,
            detail='Password and Confirm password do not match')
    hashed_password = auth_service.get_password_hash(user.password)
    user.password = hashed_password
    del user.confirmPassword
    user_collection.insert_one(jsonable_encoder(user))
    del user.password
    return {"data": user,
            "message": "user created successfully"}


def login_user(user):
    user_found = None
    get_user = user_collection.find_one({"email": user.email})
    if get_user:
        user_found = get_user
    if (user_found is None) or (not auth_service.verify_password(
            user.password, user_found['password'])):
        raise HTTPException(status_code=401,
                            detail='Invalid email and/or password')

    token = auth_service.encode_token(str(user_found['_id']))
    return {'token': token}


def get_user(userid):
    currentUser = user_collection.find_one({'_id': ObjectId(userid)})
    return {"data": user_helper(currentUser)}


def reset_password(user):
    get_user = user_collection.find_one({"email": user.email})
    if(get_user):
        if(user.password != user.confirmPassword):
            raise HTTPException(
                status_code=400,
                detail='Password and Confirm password do not match')
        hashed_password = auth_service.get_password_hash(user.password)
        get_user["password"] = hashed_password
        user_collection.save(get_user)
        return {"data": get_user['email'],
                'message': 'Password reset successfully'}
    else:
        raise HTTPException(status_code=401, detail='Invalid email')
