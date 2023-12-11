from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
uri = os.environ.get("URI")
client = MongoClient(uri)
db = client["school"]
student_records_collection = db['student_records']