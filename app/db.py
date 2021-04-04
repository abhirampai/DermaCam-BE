import pymongo
import os
from pymongo import MongoClient
from dotenv import dotenv_values, find_dotenv

config = dotenv_values(find_dotenv())

cluster = MongoClient(config["MONGO_URL"] or os.environ.get("MONGO_URL"))
db = cluster[config["DATABASE"] or os.environ.get("DATABASE")]
user_collection = db[config["USERS"] or os.environ.get("USERS")]
image_collection = db[config["IMAGES"] or os.environ.get("IMAGES")]
