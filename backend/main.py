from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId
from database import collection

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def user_helper(user):
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"]
    }

@app.post("/users")
async def create_user(user: dict):
    result = collection.insert_one(user)
    return {
        "message": "User created",
        "id": str(result.inserted_id)
    }

@app.get("/users")
async def get_users():
    users = []
    for user in collection.find():
        users.append(user_helper(user))
    return users

@app.put("/users/{id}")
async def update_user(id: str, user: dict):
    collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": user}
    )
    return {"message": "User updated"}

@app.delete("/users/{id}")
async def delete_user(id: str):
    collection.delete_one({"_id": ObjectId(id)})
    return {"message": "User deleted"}
