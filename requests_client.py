import requests
from pprint import pprint


host = "http://127.0.0.1:8000"


def add_user():
    r = requests.post(url=host + "/new_user")
    pprint(r.json())


def edit_user():

    data = {
        "user_id": "0",
        "money": "10",
        "crystals": "10"
    }

    r = requests.post(url=host + "/admin/edit/0", data=data)
    pprint(r.json())


if __name__ == "__main__":
    # post_edit_user()
    add_user()
