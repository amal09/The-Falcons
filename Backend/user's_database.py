from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pydantic import BaseModel
import hashlib, binascii, os
from bson import ObjectId



# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client.Medication
users_collection = db.Users

# FastAPI app
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# User model
class User(BaseModel):
    email: str
    password: str

# Sign-up endpoint
@app.post("/api/v1/signup")
async def signup(user: User):
    # check if user already exists
    if users_collection.count_documents({'email': user.email}) > 0:
        raise HTTPException(status_code=409, detail='Email already exists')

    # hash the password
    hashed_password = hash_password(user.password)

    # create the user document
    user_doc = {'email': user.email, 'password': hashed_password}

    # insert the user document into the database
    result = users_collection.insert_one(user_doc)

    # return the inserted user's ID
    return {'id': str(result.inserted_id)}

# Login endpoint
@app.post("/api/v1/login")
async def login(user: User):
    # retrieve the user document from the database
    user_doc = users_collection.find_one({'email': user.email})

    # check if user exists
    if user_doc is None:
        raise HTTPException(status_code=401, detail='Invalid email or password')

    # check if password is correct
    if not verify_password(user.password, user_doc['password']):
        raise HTTPException(status_code=401, detail='Invalid email or password')

    # return success message
    return {'message': 'Login successful'}


def hash_password(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def verify_password(stored_password, provided_password):
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  provided_password.encode('utf-8'), 
                                  salt.encode('ascii'), 100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password




# Define the MedicalHistory model
class MedicalHistory(BaseModel):
    user_id: str
    details: str

# Create a new user
@app.post("/api/v1/users")
def create_user(user: User):
    user_collection = db.users
    result = user_collection.insert_one(user.dict())
    return {"message": "User created successfully.", "user_id": str(result.inserted_id)}

# Get a user by ID
@app.get("/api/v1/users/{user_id}")
def get_user(user_id: str):
    user_collection = db.users
    user = user_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return {"user_id": user.get("user_id"), "password": user.get("password")}
    else:
        raise HTTPException(status_code=404, detail="User not found.")

# Create a medical history entry
@app.post("/api/v1/medical_history")
def create_medical_history(history: MedicalHistory):
    history_collection = db.history
    result = history_collection.insert_one(history.dict())
    return {"message": "Medical history created successfully.", "history_id": str(result.inserted_id)}

# Get medical history for a user
@app.get("/api/v1/medical_history/{user_id}")
def get_medical_history(user_id: str):
    history_collection = db.history
    history = history_collection.find_one({"user_id": user_id})
    if history:
        return {"user_id": history.get("user_id"), "details": history.get("details")}
    else:
        raise HTTPException(status_code=404, detail="Medical history not found.")
    
print("runiingggg///   ")
# from pymongo import MongoClient

# create a client object
client = MongoClient('mongodb://localhost:27017/')

# get the database instance
db = client['Medication']

# test the connection by getting the list of available collections in the database
collection_names = db.list_collection_names()
print(collection_names)