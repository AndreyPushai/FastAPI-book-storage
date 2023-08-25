from typing import Literal
from pydantic import BaseModel, Field
from datetime import datetime
from fastapi import HTTPException


facility_data = {
    1: {"price": 100, "construction_time": 60},
    2: {"price": 200, "construction_time": 180},
    3: {"price": 400, "construction_time": 1800},
    4: {"price": 600, "construction_time": 2400},
    5: {"price": 1200, "construction_time": 6400}
}


class Facility(BaseModel):
    type: Literal["MoneyFacility", "CrystalsFacility"]
    price: int
    construction_time: int
    level: int


class MoneySpawnFacility(Facility):

    type: str = Field(default="MoneyFacility")
    price: int = Field(default=10)
    construction_time: int = Field(default=60)
    spawn_time: int = Field(default=60)
    level: int = Field(default=1, ge=1, le=5)
    money: int = Field(default=0)


    def spawn_money(self):
        match self.level:
            case 1:
                print("Starting money generation...")
                self.money = 10
            case other:
                raise Exception("level mismatch.")


    def collect_money(self, user_money: int):
        user_money = user_money + self.money
        self.money = 0
        self.spawn_money()


class CrystalsSpawnFacility(Facility):
    type: str = Field(default="CrystalsFacility")
    price: int = Field(default=10)
    construction_time: int = Field(default=60)
    level: int = Field(default=1, ge=1, le=5)
    money: int = Field(default=0)


class UserBase(BaseModel):
    # max per level?
    money: int = Field(default=0)
    crystals: int = Field(default=0)
    facilities: list = Field(default=[])


    def set_money(self, value: int):
        self.money = value


    def set_crystals(self, value: int):
        self.crystals = value


    def build_money_facility(self):
        price = MoneySpawnFacility().price
        if self.money < price:
            raise HTTPException(status_code=422, detail=f"Not enough money!")

        self.set_money(self.money - price)
        self.facilities.append(MoneySpawnFacility())


    def build_crystals_facility(self):
        price = MoneySpawnFacility().price
        if self.money < price:
            raise HTTPException(status_code=422, detail=f"Not enough money!")

        self.set_money(self.money - price)
        self.facilities.append(MoneySpawnFacility())


    def get_facility(self, type: str, level: int):
        try:
            facility = next(facility for facility in self.facilities if facility.type == type)
        except StopIteration:
            raise HTTPException(status_code=422, detail=f"Facility {type=} not found.")
        else:
            return facility

    # forces
    # defence
