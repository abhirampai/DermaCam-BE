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
cluster = MongoClient(MongoURL)
db = cluster[db_config]
user_collection = db[user_collection_config]
image_collection = db[image_collection_config]
cloudinary.config( 
  cloud_name = config["CLOUDNAME"], 
  api_key = config["CLOUDINARYAPI"], 
  api_secret = config["CLOUDINARYAPISECRET"] 
)