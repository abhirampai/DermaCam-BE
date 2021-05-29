import pymongo
import os
from pymongo import MongoClient
from dotenv import dotenv_values, find_dotenv
import cloudinary
import cloudinary.uploader
import cloudinary.api

config = dotenv_values(find_dotenv())
MongoURL = os.environ.get("MONGO_URL") or config["MONGO_URL"]
db_config = os.environ.get("DATABASE") or config["DATABASE"]
user_collection_config = os.environ.get("USERS") or config["USERS"]
image_collection_config = os.environ.get("IMAGES") or config["IMAGES"]
product_collection_config = os.environ.get("PRODUCTS") or config["PRODUCTS"]
doctor_collection_config = os.environ.get("DOCTORS") or config["DOCTORS"]
cluster = MongoClient(MongoURL)
db = cluster[db_config]
user_collection = db[user_collection_config]
image_collection = db[image_collection_config]
product_collection = db[product_collection_config]
doctor_collection = db[doctor_collection_config]
key = os.environ.get("GOOGLEAPI") or config["GOOGLEAPI"]
cloudinary.config(
    cloud_name=os.environ.get("CLOUDNAME") or config["CLOUDNAME"],
    api_key=os.environ.get("CLOUDINARYAPI") or config["CLOUDINARYAPI"],
    api_secret=os.environ.get("CLOUDINARYAPISECRET") or config["CLOUDINARYAPISECRET"]
)
