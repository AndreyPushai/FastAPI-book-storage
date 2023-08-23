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


if __name__ == "__main__":
    id = add_user()
    edit_user(id)
