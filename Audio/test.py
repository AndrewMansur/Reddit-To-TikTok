from dotenv import load_dotenv, find_dotenv
import os
from pymongo import MongoClient
load_dotenv(find_dotenv())

password = os.environ.get("MONGODB_PWD")

connection_string = "mongodb+srv://andrewmansur4: andrew1497@tiktokautomation.lng1ogw.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_string)