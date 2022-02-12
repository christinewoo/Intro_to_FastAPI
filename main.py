from http.client import HTTPException
from typing import List
from uuid import UUID
from fastapi import FastAPI, HTTPException
from models import User, Gender, Role, UpdateFields

app = FastAPI()

# DATABASE: for now..can be connected to actual data base later
db: List[User] = [
    User(
        id=UUID("7a5927ae-02c9-4e1a-915c-a121bf44b2b4"), 
        first_name="Wheein",
        last_name="Jung",
        gender = Gender.female,
        roles = [Role.singer, Role.dancer]
    ),
    User(
        id=UUID("1cfaa091-de3c-4fb1-95f8-d28ecfb81aa5"), 
        first_name="Hyejin",
        last_name="Ahn",
        gender = Gender.female,
        roles = [Role.singer, Role.rapper, Role.user, Role.admin]
    ),
    User(
        id=UUID("af68e8b5-8a2f-4feb-b323-b3eb603b40f1"), 
        first_name="Yongsun",
        last_name="Kim",
        gender = Gender.female,
        roles = [Role.singer, Role.leader]
    )
    # User(
    #     id=UUID("a573268c-8748-4dea-bd44-7c70f944ef5c"), 
    #     first_name="Byulyi",
    #     last_name="Moon",
    #     gender = Gender.female,
    #     roles = [Role.rapper, Role.dancer]
    # )
]


# Route for get request - specify path in ()
# Get Request: retrieves data
@app.get("/") # local host 8000
async def root(): 
    return {"Hello": "Christine"} # RETURN object (dictionary)

# Define route to get list of Users and expose to clients
@app.get("/api/v1/users")
async def fetch_users():
    return db

# Submit a new User
@app.post("/api/v1/users")
async def register_user(user: User):
    db.append(user)
    return {"id": user.id} # Send to client the id of that user

# How to send post request to our API?
#   1. user the thunder client
#   2. /docs is interactive
#   3. /redoc is not interactive but can download

# How to delete a user
@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return
    raise HTTPException(
        status_code = 404,
        detail= f"user with id: {user_id} does not exist"
    )

# Handle deletion of a NULL database db
@app.put("/api/v1/users/{user_id}")
async def update_user(user_id: UUID, updates: UpdateFields):
    for user in db:
        if user.id == user_id:
            if updates.first_name is not None:
                user.first_name = updates.first_name
            
            if updates.last_name is not None:
                user.last_name = updates.last_name
            
            if updates.middle_name is not None:
                user.middle_name = updates.middle_name
            
            if updates.roles is not None:
                user.roles = updates.roles
            return
    raise HTTPException(
        status_code = 404,
        detail= f"user with id: {user_id} does not exist"
    )