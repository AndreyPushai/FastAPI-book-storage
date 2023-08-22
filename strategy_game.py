from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
import time

app = FastAPI()


class UserBase(BaseModel):
    # max per level?
    money: int = Field(default=0)
    crystals: int = Field(default=0)


    def set_money(self, value: int):
        self.money = value


    def set_crystals(self, value: int):
        self.crystals = value

    # forces
    # defence


class User(BaseModel):
    def set_id():
        return time.time_ns()

    id: int = Field(default_factory=set_id)
    base: UserBase = Field(default_factory=UserBase)


users = [
    User(),
    User(),
    User(),
    User()
]


def get_user_by_id(user_id: int):
    # try:
    print("DBG")
    print(user_id)
    print([user.id for user in users])
    print()
    user = next(user for user in users if user.id == user_id)
    #         if user.id == user_id:
    #             return user
    # except StopIteration:
    #     raise Exception(f"User with {user_id=} not found.")
    # else:
    return user


@app.get("/")
def welcome_query():
    return "Welcome to the game. To create user: POST /new_user"


@app.get("/admin/users")
def get_users_query():
    for user in users:
        print("DBG")
        print(user.id)

    return users


@app.get("/{user_id}")
def get_user_info_query(user_id) -> User:
    return get_user_by_id(user_id)


@app.post("/new_user")
def add_user():
    users.append(User())


@app.put("/admin/edit/{user_id}")
def edit_user_query(
            user_id: int,
            money: int | None = None,
            crystals: int | None = None):

    user: User = get_user_by_id(user_id)

    if user is None:
        raise HTTPException(status_code=400, detail=f"User with {user_id=} not found.")

    if money is not None:
        user.base.money = money

    if crystals is not None:
        user.base.crystals = crystals
