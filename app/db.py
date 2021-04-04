import pymongo
import os
from pymongo import MongoClient
from dotenv import dotenv_values, find_dotenv

config = dotenv_values(find_dotenv())
cluster = MongoClient(os.environ.get("MONGO_URL"))
db = cluster[os.environ.get("DATABASE")]
user_collection = db[os.environ.get("USERS")]
image_collection = db[os.environ.get("IMAGES")]
