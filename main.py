from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="User API Project", version="1.0")

users = []
user_id_counter = 1

class User(BaseModel):
    name: str
    email: str
    phone_number: str


@app.post("/users")
def create_user(user: User):
    global user_id_counter
    new_user = user.dict()
    new_user["id"] = user_id_counter
    users.append(new_user)
    user_id_counter += 1
    return {"message": "User created successfully", "user": new_user}


@app.get("/users")
def get_users():
    return {"users": users}


@app.put("/users/{user_id}")
def update_user(user_id: int, user: User):
    for u in users:
        if u["id"] == user_id:
            u["name"] = user.name
            u["email"] = user.email
            u["phone_number"] = user.phone_number
            return {"message": "User updated successfully", "user": u}
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    for u in users:
        if u["id"] == user_id:
            users.remove(u)
            return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")
