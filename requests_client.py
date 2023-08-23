import requests
from pprint import pprint


host = "http://127.0.0.1:8000"


def add_user():
    r = requests.post(url=host + "/new_user")
    pprint(r.json())
    return r.json()["id"]


def edit_user(user_id: int):

    json = {
        "money": 10,
        "crystals": 10
    }

    r = requests.put(url=host + f"/admin/edit/{user_id}", json=json)
    pprint(r.json())


def add_money_facility(user_id: int):
    r = requests.put(url=host + f"/users/{user_id}/add_money_facility")
    pprint(r.json())


if __name__ == "__main__":
    id = add_user()
    edit_user(id)
    add_money_facility(id)
