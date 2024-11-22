from typing import Annotated, Literal

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()


# update a user name and password
class UpdateUser(BaseModel):
    username: str = Field(..., title="username")
    password: str = Field(..., title="password")


# update a user name and password
@app.put("/update_user/")