from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
from player_base import PlayerBase
from utils.time_generator import ns_timestamp


app = FastAPI()


class Player(BaseModel):
    id: int = Field(default_factory=ns_timestamp)
    base: PlayerBase = Field(default_factory=PlayerBase)


users = [
    Player(),
    Player(),
    Player(),
    Player()
]


def get_user_by_id(user_id: int):
    try:
        user = next(user for user in users if user.id == user_id)
    except StopIteration:
        raise HTTPException(status_code=400, detail=f"Player with {user_id=} not found.")
    else:
        return user


@app.get("/")
def welcome_query():
    return "Welcome to the game. To create user: POST /new_user"


@app.get("/users")
def get_users_query():
    return users


@app.get("/users/{user_id}")
def get_user_info_query(user_id: int) -> Player:
    return get_user_by_id(user_id)


@app.post("/new_user")
def add_user():
    new_user = Player()
    users.append(new_user)
    return new_user


@app.put("/admin/edit/{user_id}")
def edit_user_base_query(user_id: int, base: PlayerBase):
    user = get_user_by_id(user_id)
    user.base = base
    return user


@app.put("/users/{user_id}/add_money_facility")
def add_money_facility_query(user_id: int):
    user = get_user_by_id(user_id)
    user.base.build_money_facility()
    return user
