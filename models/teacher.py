from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
uri = os.environ.get("URI")
client = MongoClient(uri)
db = client["school"]
teacher_collection = db['teacher']
subjects_collection = db['subjects']