from ..db import user_collection,product_collection
from .auth_service import AuthHandler
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from bson.objectid import ObjectId
from tensorflow.keras.models import load_model
from keras.preprocessing import image
import urllib.request
import cv2
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
import numpy as np
model_file = "app/model/DiseaseDetectionModel.h5"
severity_file = "app/model/SeverityModel.h5"
auth_service = AuthHandler()


def user_helper(user) -> dict:
    return {
        "user_id": str(user["_id"]),
        "email": user["email"],
        "firstName": user["firstName"],
        "lastName": user["lastName"],
    }

def product_helper(product) -> dict:
    return {
        "product_name":product["product_name"],
        "brand":product["brand"],
        "brand_link":product["brand_link"],
        "ingredients": product["ingredients"],
        "image": product["image"],
        "cures": product["cures"]
    }

def user_health_status(user) -> dict:
    return {
        "patient_data": user["patient_data"]
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
    new_user = jsonable_encoder(user)
    new_user["healthDetailStatus"] = 0
    user_collection.insert_one(new_user)
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


def add_patient_details(userid, patient_data):
    currentUser = user_collection.find_one({'_id': ObjectId(userid)})
    if currentUser["healthDetailStatus"] == 0:
        currentUser["patient_data"] = jsonable_encoder(patient_data)
        currentUser["healthDetailStatus"] = 1
        user_collection.save(currentUser)
        return {"data": user_helper(currentUser)}
    else:
        raise HTTPException(
            status_code=400,
            detail='Details Already Entered')


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


def get_health_detail_status(userid):
    currentUser = user_collection.find_one({'_id': ObjectId(userid)})
    if(currentUser["healthDetailStatus"] == 1):
        return {
            "data": True
        }
    else:
        return {
            "data": False
        }


def get_user_health_detail(userid):
    current_user = user_collection.find_one({'_id': ObjectId(userid)})
    try:
        if(current_user["patient_data"]):
            return {
                "data": user_health_status(current_user)
            }
    except:
        raise HTTPException(status_code=401, detail='Health details not entered')

def get_user_disease_detail(imageUrl):
    detectionModel = load_model(model_file)
    resp = urllib.request.urlopen(imageUrl)
    imageUploaded = np.asarray(bytearray(resp.read()), dtype="uint8")
    test_image = cv2.imdecode(imageUploaded, cv2.IMREAD_COLOR)
    resized_shape = (64,64)
    test_img = cv2.resize(test_image,(resized_shape[1],resized_shape[0]))
    skinDiseaseTypes=['blackhead', 'Acne', 'kutil filiform', 'flek hitam', 'folikulitis', 'milia', 'Dermatitis perioral', 'Karsinoma', 'panu', 'melanoma', 'herpes', 'Eksim', 'papula', 'whitehead', 'Tinea facialis', 'rosacea', 'Pustula', 'psoriasis']
    x = image.img_to_array(test_img)
    x = np.expand_dims(x, axis = 0)

    x /= 255

    custom = detectionModel.predict(x)
    x = np.array(x, 'float32')
    a=custom[0]
    ind=np.argmax(a)
    if(skinDiseaseTypes[ind] == 'Acne'):
        severityModel = load_model(severity_file)
        severityLevel=['Level_0', 'Level_2', 'Level_1']
        custom = severityModel.predict(x)
        x = np.array(x, 'float32')
        a=custom[0]
        index=np.argmax(a)
        if(severityLevel[index]=="Level_0"):
            products=product_collection.find({'cures':skinDiseaseTypes[ind]})
            result=[]
            for i in products:
                result.append(product_helper(i))
            return {
                "Prediction":skinDiseaseTypes[ind],
                "SeverityLevel":severityLevel[index],
                "Suggested_Products":result
            }
        else:
            return {
            "Prediction":skinDiseaseTypes[ind],
            "SeverityLevel":severityLevel[index],
            "Suggestion":"Please consult nearby doctors"
            }
    return {
        "Prediction":skinDiseaseTypes[ind],
        "Suggestion":"Please consult nearby doctors"
        }