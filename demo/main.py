"""
This module provides API endpoints for managing employees.
"""

from typing import Annotated
from uuid import UUID, uuid4
from fastapi import FastAPI, HTTPException, status, Body, Query, Path, Request
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, EmailStr, Field
from db.data import users_db


app = FastAPI()


# pydantic modle for employee
class User(BaseModel):
    Id: UUID
    username: str
    full_name: str
    email: EmailStr
    address: str
    password: str
    # confirm_password: password
    # created_at: Optional[current_time]


# response model


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UpdateUser(BaseModel):
    username: str = Field(..., title="username")
    password: str = Field(..., title="password")


# Create user
@app.post("/create_user/", status_code=status.HTTP_201_CREATED)
async def create_user(
    new_user: Annotated[User, Body(...)], new_user_id: UUID = uuid4()
):
    for _, users in users_db.items():
        if (
            users.get("email") == new_user.email
            or users.get("username") == new_user.username
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email or username already registered",
            )
    # Create new user entry
    new_user_id = uuid4()
    users_db[new_user_id] = new_user.model_dump()
    return {"user_id": new_user_id, "user": users_db[new_user_id]}


# Login user_2
@app.post("/login_user/", status_code=status.HTTP_200_OK)
async def login_user(user_login: Annotated[UserLogin, Body(...)]):
    for user_id, user_data in users_db.items():
        user_id = str(user_id)
        if user_data["email"] == user_login.email:
            if user_data["password"] == user_login.password:
                username = user_data["username"]
                return {"welcome": f"Welcome {username}"}
            raise HTTPException(status_code=401, detail="Incorrect password")
    raise HTTPException(status_code=404, detail="User not found")


# Update user
@app.put("/update_user/{user_id}/", status_code=status.HTTP_200_OK)
async def update_user(
    email: EmailStr,
    updated_user: Annotated[UpdateUser, Body(...)],
    user_id: UUID = uuid4(),
):
    user_id = str(user_id)

    if user_id not in users_db:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    user = users_db[user_id]
    if user["email"] != email:
        raise HTTPException(status_code=400, detail="Incorrect email for this user")

    print("Email found, now update your details")
    users_db[user_id].update(updated_user.model_dump())
    return {"user_id": user_id, "user": users_db[user_id]}
