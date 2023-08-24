from pydantic import BaseModel, Field
from datetime import datetime
from fastapi import HTTPException



class MoneySpawnFacility(BaseModel):

    type: str = Field(default="MoneyFacility")
    price: int = Field(default=10)
    build_time: int = Field(default=60)
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

        self.money -= price
        self.facilities.append(MoneySpawnFacility())

    # forces
    # defence
