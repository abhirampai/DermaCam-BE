import pymongo
from pymongo import MongoClient
from dotenv import dotenv_values,find_dotenv

config=dotenv_values(find_dotenv())

cluster = MongoClient(config["MONGO_URL"])
db = cluster[config["DATABASE"]]
user_collection = db[config["USERS"]]
image_collection = db[config["IMAGES"]]